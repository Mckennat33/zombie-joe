"""Turns raw input into per-player actions, so Player never touches the keyboard."""

import json
from dataclasses import dataclass

import pygame

from game.settings import DATA_DIR


@dataclass
class Actions:
    """What one player wants to do this frame."""
    move: pygame.Vector2
    shoot: bool = False  # True only on the frame the button goes down (one press = one shot)


def load_bindings(num_players):
    """Solo uses one combined layout (WASD + arrows); co-op gives each player their own."""
    with open(DATA_DIR / "controls.json") as f:
        config = json.load(f)
    if num_players == 1:
        return [config["solo"]]
    return config["coop"][:num_players]


class KeyboardControls:
    """One player's keyboard bindings. Each action can have several keys."""

    def __init__(self, bindings):
        # Convert names like "w" or "up" into pygame key codes.
        self.keys = {
            action: [pygame.key.key_code(name) for name in names]
            for action, names in bindings.items()
        }
        self.shoot_was_held = False

    def _held(self, pressed, action):
        return any(pressed[key] for key in self.keys[action])

    def get_actions(self):
        pressed = pygame.key.get_pressed()
        move = pygame.Vector2(
            self._held(pressed, "right") - self._held(pressed, "left"),
            self._held(pressed, "down") - self._held(pressed, "up"),
        )
        if move.length_squared() > 0:
            move = move.normalize()  # so diagonals aren't faster
        # Only count a new press, so holding the button doesn't keep firing.
        shoot_held = self._held(pressed, "shoot")
        shoot = shoot_held and not self.shoot_was_held
        self.shoot_was_held = shoot_held
        return Actions(move=move, shoot=shoot)
