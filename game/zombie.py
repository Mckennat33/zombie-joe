"""A zombie that walks toward the nearest player. Stats come from data/zombies.json."""

import pygame

from game.settings import ZOMBIE_COLOR


class Zombie:
    def __init__(self, stats, pos):
        self.pos = pygame.Vector2(pos)
        self.speed = stats["speed"]
        self.health = stats["health"]
        self.size = stats["size"]
        self.color = ZOMBIE_COLOR

    @property
    def alive(self):
        return self.health > 0

    @property
    def rect(self):
        r = pygame.Rect(0, 0, self.size, self.size)
        r.center = self.pos
        return r

    def update(self, dt, players):
        target = min(players, key=lambda p: self.pos.distance_squared_to(p.pos))
        to_target = target.pos - self.pos
        if to_target.length_squared() > 0:
            self.pos += to_target.normalize() * self.speed * dt

    def take_hit(self, damage):
        self.health -= damage

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
