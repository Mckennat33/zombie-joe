"""Owns the window and the main loop."""

import json
import random

import pygame

from game.controls import KeyboardControls, load_bindings
from game.effects import BloodSplat, Disintegrate, Impact
from game.hud import HUD
from game.player import Player
from game.settings import BG_COLOR, DATA_DIR, FPS, SCREEN_HEIGHT, SCREEN_WIDTH, SPAWN_MARGIN, TITLE
from game.zombie import Zombie


class Game:
    def __init__(self, num_players=1):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.hud = HUD()

        center = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.players = []
        self.controls = []
        for i, bindings in enumerate(load_bindings(num_players)):
            self.players.append(Player(i, center + (i * 60, 0)))
            self.controls.append(KeyboardControls(bindings))

        self.bullets = []
        self.effects = []
        self.zombies = []

        with open(DATA_DIR / "zombies.json") as f:
            zombie_data = json.load(f)
        self.zombie_types = zombie_data["types"]
        self.spawning = zombie_data["test_spawning"]  # replaced by waves in M4
        self.spawn_timer = 0.0

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # seconds since last frame
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self, dt):
        # Screen edges act as walls for now; the Tiled map's walls replace this in M7.
        bounds = self.screen.get_rect()

        for player, controls in zip(self.players, self.controls):
            bullet = player.update(controls.get_actions(), dt, bounds)
            if bullet:
                self.bullets.append(bullet)

        self.update_spawning(dt)
        for zombie in self.zombies:
            zombie.update(dt, self.players)

        for bullet in self.bullets:
            bullet.update(dt)
            self.check_bullet_hits(bullet)
            if bullet.alive and not bounds.collidepoint(bullet.pos):
                # Hit a "wall": explode right at the edge.
                edge_x = max(bounds.left, min(bullet.pos.x, bounds.right - 1))
                edge_y = max(bounds.top, min(bullet.pos.y, bounds.bottom - 1))
                self.effects.append(Impact((edge_x, edge_y)))
                bullet.alive = False

        for effect in self.effects:
            effect.update(dt)

        self.bullets = [b for b in self.bullets if b.alive]
        self.effects = [e for e in self.effects if e.alive]
        self.zombies = [z for z in self.zombies if z.alive]

    def update_spawning(self, dt):
        """Temporary spawner: one zombie every few seconds, up to a max. Waves replace this in M4."""
        self.spawn_timer -= dt
        if self.spawn_timer <= 0 and len(self.zombies) < self.spawning["max_alive"]:
            self.spawn_timer = self.spawning["seconds_between_spawns"]
            stats = self.zombie_types[self.spawning["type"]]
            self.zombies.append(Zombie(stats, random_offscreen_point()))

    def check_bullet_hits(self, bullet):
        if not bullet.alive:
            return
        for zombie in self.zombies:
            if zombie.alive and zombie.rect.collidepoint(bullet.pos):
                bullet.alive = False  # bullets are used up on hit
                zombie.take_hit(bullet.damage)
                self.effects.append(BloodSplat(bullet.pos, bullet.velocity))
                if not zombie.alive:
                    # Swap the zombie for a crumbling version of itself.
                    self.effects.append(Disintegrate(zombie.rect, zombie.color))
                return

    def draw(self):
        self.screen.fill(BG_COLOR)
        for zombie in self.zombies:
            zombie.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for effect in self.effects:
            effect.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)
        self.hud.draw(self.screen, self.players)
        pygame.display.flip()


def random_offscreen_point():
    """A random spot just outside one of the four screen edges."""
    edge = random.choice(["top", "bottom", "left", "right"])
    if edge == "top":
        return (random.uniform(0, SCREEN_WIDTH), -SPAWN_MARGIN)
    if edge == "bottom":
        return (random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT + SPAWN_MARGIN)
    if edge == "left":
        return (-SPAWN_MARGIN, random.uniform(0, SCREEN_HEIGHT))
    return (SCREEN_WIDTH + SPAWN_MARGIN, random.uniform(0, SCREEN_HEIGHT))
