from pathlib import Path

#Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"
BASE_DIR = Path(__file__).resolve().parent.parent

#Constants used to scale our sprites from their original size
TILE_SCALING = 1
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.5
PLAYER_JUMP_SPEED = 14.14

#Constants used to track the direction a character is facing
RIGHT_FACING = 0
LEFT_FACING = 1

#Maps Constants
CURRENT_MAP = "nivel5.tmj"
MAP_FILE = BASE_DIR / "assets" / "maps" / CURRENT_MAP
MAPS_DIR = BASE_DIR / "assets" / "maps"

def obtener_ruta_mapa(numero_nivel):
    """Devuelve la ruta absoluta del nivel solicitado"""
    return MAPS_DIR / f"nivel{numero_nivel}.tmj"

#Astronaut Constants
CHARACTER_SCALING = 1.5
ASTRONAUT_PATH = BASE_DIR / "assets" / "sprites" / "astronaut"

#Zombie Constants
ZOMBIE_PATH = BASE_DIR / "assets" / "sprites" / "zombie"
ZOMBIE_VISION_RANGE = 150
ZOMBIE_CHASE_SPEED = 3.0
ZOMBIE_PATROL_SPEED = 1.0

#Alien Constants
ALIEN_PATH = BASE_DIR / "assets" / "sprites" / "brainAlien"
ALIEN_VISION_RANGE = 100
ALIEN_PATROL_SPEED = 1.5
ALIEN_BULLET_SPEED = 1.0
ALIEN_FIRE_RATE = 90

#Projectile Constants
PROJECTILE_PATH = BASE_DIR / "assets" / "sprites" / "proyectiles"

#Flags
TEST_LEVEL = False

