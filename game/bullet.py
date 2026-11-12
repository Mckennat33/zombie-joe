"""A single bullet flying in a straight line."""

import pygame

from game.settings import BULLET_COLOR, BULLET_RADIUS


class Bullet:
    def __init__(self, pos, velocity, damage, max_range):
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(velocity)
        self.damage = damage
        self.distance_left = max_range
        self.alive = True

    def update(self, dt):
        step = self.velocity * dt
        self.pos += step
        self.distance_left -= step.length()
        if self.distance_left <= 0:
            self.alive = False  # ran out of range: just vanish

    def draw(self, surface):
        pygame.draw.circle(surface, BULLET_COLOR, self.pos, BULLET_RADIUS)
