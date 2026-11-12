"""Engine constants: screen, timing, colors. Gameplay numbers go in data/*.json."""

from pathlib import Path

TITLE = "Zombie Joe"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 32

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
MAPS_DIR = ROOT_DIR / "maps"
ASSETS_DIR = ROOT_DIR / "assets"
SAVES_DIR = ROOT_DIR / "saves"

# Colors
BG_COLOR = (40, 44, 40)
PLAYER_COLORS = [(70, 130, 220), (220, 160, 60)]  # player 1, player 2

# Bullets and impact effect (visuals only; damage/speed live in data/weapons.json)
BULLET_RADIUS = 3
BULLET_COLOR = (255, 220, 50)
IMPACT_DURATION = 0.25  # seconds
IMPACT_SPARKS = 8
IMPACT_SPARK_SPEED = 120  # pixels per second
IMPACT_COLORS = [(255, 240, 150), (255, 150, 40)]  # core flash, sparks

# HUD
HUD_MARGIN = 16
HUD_FONT_SIZE = 30
HUD_TEXT_COLOR = (240, 240, 240)
HEALTH_BAR_SIZE = (200, 16)
HEALTH_BAR_COLOR = (210, 40, 40)
HEALTH_BAR_BG_COLOR = (70, 20, 20)
HEART_SIZE = 22
HEART_COLOR = (220, 40, 60)
HEART_LOST_COLOR = (80, 80, 80)
