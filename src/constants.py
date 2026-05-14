from pathlib import Path

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 1
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# Constants used to track the direction a character is facing
RIGHT_FACING = 0
LEFT_FACING = 1

CURRENT_MAP = "nivel-prueba.tmj"
BASE_DIR = Path(__file__).resolve().parent.parent
MAP_FILE = BASE_DIR / "assets" / "maps" / CURRENT_MAP

#Astronaut's constants
CHARACTER_SCALING = 1.5
ASTRONAUT_PATH = BASE_DIR / "assets" / "sprites" / "astronaut"