"""Short visual effects, like the little explosion when a bullet hits a wall."""

import random

import pygame

from game.settings import IMPACT_COLORS, IMPACT_DURATION, IMPACT_SPARK_SPEED, IMPACT_SPARKS


class Impact:
    """A quick flash plus a few sparks flying outward, then gone."""

    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.age = 0.0
        self.sparks = [
            pygame.Vector2(random.uniform(0.4, 1) * IMPACT_SPARK_SPEED, 0).rotate(random.uniform(0, 360))
            for _ in range(IMPACT_SPARKS)
        ]

    @property
    def alive(self):
        return self.age < IMPACT_DURATION

    def update(self, dt):
        self.age += dt

    def draw(self, surface):
        fade = 1 - self.age / IMPACT_DURATION  # 1 at start, 0 at end
        core_color, spark_color = IMPACT_COLORS
        pygame.draw.circle(surface, core_color, self.pos, 7 * fade)
        for velocity in self.sparks:
            pygame.draw.circle(surface, spark_color, self.pos + velocity * self.age, max(1, 3 * fade))
