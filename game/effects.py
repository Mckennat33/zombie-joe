"""Short visual effects: bullet impacts, blood splats, zombies crumbling away.

Every effect has update(dt), draw(surface) and an `alive` flag, so Game can treat them all the same.
"""

import random

import pygame

from game.settings import (
    BLOOD_COLORS, BLOOD_DROPS, BLOOD_DURATION, BLOOD_SPEED, BLOOD_SPREAD,
    DISINTEGRATE_DRIFT, DISINTEGRATE_DURATION, DISINTEGRATE_GRID,
    IMPACT_COLORS, IMPACT_DURATION, IMPACT_SPARK_SPEED, IMPACT_SPARKS,
)


class Effect:
    """Base class: tracks age and dies after `duration` seconds."""

    duration = 1.0

    def __init__(self):
        self.age = 0.0

    @property
    def alive(self):
        return self.age < self.duration

    @property
    def fade(self):
        """1 at the start, 0 at the end."""
        return max(0.0, 1 - self.age / self.duration)

    def update(self, dt):
        self.age += dt


class Impact(Effect):
    """Bullet hits a wall: a quick flash plus a few sparks flying outward."""

    duration = IMPACT_DURATION

    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.sparks = [
            pygame.Vector2(random.uniform(0.4, 1) * IMPACT_SPARK_SPEED, 0).rotate(random.uniform(0, 360))
            for _ in range(IMPACT_SPARKS)
        ]

    def draw(self, surface):
        core_color, spark_color = IMPACT_COLORS
        pygame.draw.circle(surface, core_color, self.pos, 7 * self.fade)
        for velocity in self.sparks:
            pygame.draw.circle(surface, spark_color, self.pos + velocity * self.age, max(1, 3 * self.fade))


class BloodSplat(Effect):
    """Zombie gets shot: red drops spray out the far side, in the bullet's direction."""

    duration = BLOOD_DURATION

    def __init__(self, pos, direction):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        direction = pygame.Vector2(direction)
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.drops = [
            (
                direction.rotate(random.uniform(-BLOOD_SPREAD, BLOOD_SPREAD)) * random.uniform(0.3, 1) * BLOOD_SPEED,
                random.choice(BLOOD_COLORS),
                random.uniform(2, 4),  # drop radius
            )
            for _ in range(BLOOD_DROPS)
        ]

    def draw(self, surface):
        for velocity, color, radius in self.drops:
            pygame.draw.circle(surface, color, self.pos + velocity * self.age, max(1, radius * self.fade))


class Disintegrate(Effect):
    """A dead zombie breaks into small squares that crumble away one by one."""

    duration = DISINTEGRATE_DURATION

    def __init__(self, rect, color):
        super().__init__()
        self.color = color
        self.piece_size = rect.width / DISINTEGRATE_GRID
        self.pieces = []
        for col in range(DISINTEGRATE_GRID):
            for row in range(DISINTEGRATE_GRID):
                start = pygame.Vector2(
                    rect.left + (col + 0.5) * self.piece_size,
                    rect.top + (row + 0.5) * self.piece_size,
                )
                drift = pygame.Vector2(random.uniform(0.3, 1) * DISINTEGRATE_DRIFT, 0).rotate(random.uniform(0, 360))
                # Each piece waits a random moment before it starts crumbling, so the body breaks up gradually.
                delay = random.uniform(0, self.duration * 0.6)
                self.pieces.append((start, drift, delay))

    def draw(self, surface):
        for start, drift, delay in self.pieces:
            t = max(0.0, self.age - delay)  # time since this piece started crumbling
            piece_fade = max(0.0, 1 - t / (self.duration - delay))
            if piece_fade == 0:
                continue
            size = self.piece_size * piece_fade
            piece = pygame.Rect(0, 0, size, size)
            piece.center = start + drift * t
            pygame.draw.rect(surface, self.color, piece)
