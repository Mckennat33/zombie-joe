"""A player character. Gets Actions from a controls object, never reads input itself."""

import json

import pygame

from game.settings import DATA_DIR, PLAYER_COLORS
from game.weapon import Weapon


class Player:
    def __init__(self, index, pos):
        with open(DATA_DIR / "player.json") as f:
            stats = json.load(f)
        self.index = index
        self.pos = pygame.Vector2(pos)
        self.speed = stats["speed"]
        self.max_health = stats["max_health"]
        self.health = self.max_health
        self.max_lives = stats["lives"]
        self.lives = self.max_lives
        self.size = stats["size"]
        self.weapon = Weapon(stats["start_weapon"])
        self.color = PLAYER_COLORS[index % len(PLAYER_COLORS)]
        self.facing = pygame.Vector2(0, -1)

    @property
    def rect(self):
        r = pygame.Rect(0, 0, self.size, self.size)
        r.center = self.pos
        return r

    def update(self, actions, dt, bounds):
        """Move, then try to shoot. Returns a new Bullet if one was fired, else None."""
        if actions.move.length_squared() > 0:
            self.facing = actions.move  # Joe shoots the way he last walked
        self.pos += actions.move * self.speed * dt
        self.keep_inside(bounds)

        self.weapon.update(dt)
        if actions.shoot:
            muzzle = self.pos + self.facing * self.size / 2
            return self.weapon.fire(muzzle, self.facing)
        return None

    def keep_inside(self, bounds):
        """Push Joe back so his whole body stays inside the bounds rect."""
        half = self.size / 2
        # Clamp the float position (not the int Rect) so slow movement isn't lost to rounding.
        self.pos.x = max(bounds.left + half, min(self.pos.x, bounds.right - half))
        self.pos.y = max(bounds.top + half, min(self.pos.y, bounds.bottom - half))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        # Small line showing which way Joe is facing.
        tip = self.pos + self.facing * self.size * 0.8
        pygame.draw.line(surface, (255, 255, 255), self.pos, tip, 3)
