"""Owns the window and the main loop."""

import pygame

from game.controls import KeyboardControls, load_bindings
from game.effects import Impact
from game.hud import HUD
from game.player import Player
from game.settings import BG_COLOR, FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE


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

        for bullet in self.bullets:
            bullet.update(dt)
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

    def draw(self):
        self.screen.fill(BG_COLOR)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for effect in self.effects:
            effect.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)
        self.hud.draw(self.screen, self.players)
        pygame.display.flip()
