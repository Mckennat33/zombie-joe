"""Top-right HUD: weapon + ammo, health bar, lives. One panel per player, stacked."""

import pygame

from game.settings import (
    HEALTH_BAR_BG_COLOR, HEALTH_BAR_COLOR, HEALTH_BAR_SIZE, HEART_COLOR, HEART_LOST_COLOR,
    HEART_SIZE, HUD_FONT_SIZE, HUD_MARGIN, HUD_TEXT_COLOR,
)

GAP = 6  # space between HUD rows


class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, HUD_FONT_SIZE)

    def draw(self, surface, players):
        top = HUD_MARGIN
        for player in players:
            top = self.draw_player(surface, player, top) + HUD_MARGIN

    def draw_player(self, surface, player, top):
        """Draw one player's panel starting at `top`; return the y where it ends."""
        right = surface.get_width() - HUD_MARGIN

        # 1. Weapon name and ammo: "Pistol  ∞" or "Rifle  30/100"
        weapon = player.weapon
        if weapon.unlimited:
            # The default font has no real ∞ glyph, so draw it as a shape.
            text = self.font.render(f"{weapon.name}  ", True, HUD_TEXT_COLOR)
            symbol = pygame.Rect(0, 0, 26, 12)
            symbol.topright = (right, top + (text.get_height() - symbol.height) // 2)
            draw_infinity(surface, symbol, HUD_TEXT_COLOR)
            text_rect = text.get_rect(topright=(symbol.left, top))
        else:
            ammo = f"{weapon.ammo_in_mag}/{weapon.reserve_ammo}"
            text = self.font.render(f"{weapon.name}  {ammo}", True, HUD_TEXT_COLOR)
            text_rect = text.get_rect(topright=(right, top))
        surface.blit(text, text_rect)

        # 2. Red health bar
        bar = pygame.Rect((0, 0), HEALTH_BAR_SIZE)
        bar.topright = (right, text_rect.bottom + GAP)
        pygame.draw.rect(surface, HEALTH_BAR_BG_COLOR, bar)
        filled = bar.copy()
        filled.width = round(bar.width * max(0, player.health) / player.max_health)
        pygame.draw.rect(surface, HEALTH_BAR_COLOR, filled)

        # 3. Hearts for lives (grey = lost), right-aligned under the bar
        heart_top = bar.bottom + GAP
        for i in range(player.max_lives):
            color = HEART_COLOR if i < player.lives else HEART_LOST_COLOR
            x = right - (player.max_lives - i) * (HEART_SIZE + GAP) + GAP
            draw_heart(surface, (x + HEART_SIZE / 2, heart_top + HEART_SIZE / 2), HEART_SIZE, color)

        return heart_top + HEART_SIZE


def draw_infinity(surface, rect, color):
    """An ∞ made of two side-by-side ring outlines filling `rect`."""
    half = rect.width // 2 + 1  # +1 so the rings overlap and touch in the middle
    pygame.draw.ellipse(surface, color, (rect.left, rect.top, half, rect.height), 2)
    pygame.draw.ellipse(surface, color, (rect.right - half, rect.top, half, rect.height), 2)


def draw_heart(surface, center, size, color):
    """A heart from two circles (the bumps) and a triangle (the point)."""
    x, y = center
    r = size / 4
    pygame.draw.circle(surface, color, (x - r, y - r / 2), r)
    pygame.draw.circle(surface, color, (x + r, y - r / 2), r)
    pygame.draw.polygon(surface, color, [(x - 2 * r, y - r / 4), (x + 2 * r, y - r / 4), (x, y + size / 2)])
