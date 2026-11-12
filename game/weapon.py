"""A gun: fire delay and ammo. Stats come from data/weapons.json."""

import json

from game.bullet import Bullet
from game.settings import DATA_DIR


class Weapon:
    def __init__(self, weapon_id):
        with open(DATA_DIR / "weapons.json") as f:
            stats = json.load(f)[weapon_id]
        self.name = stats["display_name"]
        self.damage = stats["damage"]
        self.fire_delay = stats["fire_delay"]
        self.bullet_speed = stats["bullet_speed"]
        self.range = stats["range"]
        self.magazine_size = stats["magazine_size"]  # null in JSON = unlimited ammo
        self.ammo_in_mag = self.magazine_size
        self.reserve_ammo = stats["reserve_ammo"]
        self.cooldown = 0.0  # seconds until the gun can fire again

    @property
    def unlimited(self):
        return self.magazine_size is None

    def update(self, dt):
        self.cooldown = max(0.0, self.cooldown - dt)

    def can_fire(self):
        return self.cooldown == 0 and (self.unlimited or self.ammo_in_mag > 0)

    def fire(self, pos, direction):
        """Return a new Bullet, or None if the gun isn't ready (still cooling down or empty)."""
        if not self.can_fire():
            return None
        self.cooldown = self.fire_delay
        if not self.unlimited:
            self.ammo_in_mag -= 1
        return Bullet(pos, direction * self.bullet_speed, self.damage, self.range)
