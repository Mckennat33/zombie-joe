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

# Zombies (visuals only; speed/health live in data/zombies.json)
ZOMBIE_COLOR = (125, 130, 125)
SPAWN_MARGIN = 30  # how far off-screen zombies appear

# Blood splat when a zombie is hit
BLOOD_DURATION = 0.4  # seconds
BLOOD_DROPS = 10
BLOOD_SPEED = 150  # pixels per second
BLOOD_SPREAD = 45  # degrees either side of the bullet's direction
BLOOD_COLORS = [(200, 20, 20), (130, 0, 0)]

# Dead zombies crumble into pieces that drift and shrink away
DISINTEGRATE_DURATION = 1.5  # seconds
DISINTEGRATE_GRID = 4  # zombie splits into 4x4 pieces
DISINTEGRATE_DRIFT = 20  # pixels per second

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
