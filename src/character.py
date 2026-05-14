import math
from pathlib import Path
import arcade
from constants import *
from PIL import Image

#Constantes de dirección vertical
FACE_UP = 0
FACE_FORWARD = 1
FACE_DOWN = 2
FACE_UP_DIAGONAL = 3
FACE_DOWN_DIAGONAL = 4

UPDATES_PER_FRAME = 7

def load_spritesheet_pair(path: str, frame_count: int, frame_w: int, frame_h: int, cols: int):
    frames_normales = []
    frames_volteados = []
    imagen_completa = Image.open(path)
    
    for i in range(frame_count):
        fila = i // cols
        columna = i % cols
        left   = columna * frame_w
        top    = fila * frame_h
        right  = left + frame_w
        bottom = top + frame_h
        recorte = imagen_completa.crop((left, top, right, bottom))
        textura = arcade.Texture(recorte)
        frames_normales.append(textura)
        frames_volteados.append(textura.flip_left_right())

    return frames_normales, frames_volteados

class Character(arcade.Sprite):
    def __init__(self, name_folder, name_file):
        super().__init__()

        self.facing_direction = RIGHT_FACING

        self.cur_texture = 0

        main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"
        # Load textures for idle, jump, and fall states
        idle_texture = arcade.load_texture(f"{main_path}_idle.png")
        jump_texture = arcade.load_texture(f"{main_path}_jump.png")
        fall_texture = arcade.load_texture(f"{main_path}_fall.png")
        # Make pairs with left and right facing textures
        self.idle_texture_pair = idle_texture, idle_texture.flip_left_right()
        self.jump_texture_pair = jump_texture, jump_texture.flip_left_right()
        self.fall_texture_pair = fall_texture, fall_texture.flip_left_right()
        # Load textures for walking with left and right facing textures
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture(f"{main_path}_walk{i}.png")
            self.walk_textures.append((texture, texture.flip_left_right()))

        self.climbing_textures = (
            arcade.load_texture(f"{main_path}_climb0.png"),
            arcade.load_texture(f"{main_path}_climb1.png")
        )

        # This variable will change dynamically and will represent the currently
        # active texture.
        self.texture = self.idle_texture_pair[0]


class PlayerCharacter(arcade.Sprite):
    """Jugador astronauta"""
    def __init__(self):
        super().__init__()

        self.facing_direction = RIGHT_FACING
        self.vertical_facing = FACE_FORWARD
        self.climbing = False
        self.is_on_ground = True
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        ruta_base = ASTRONAUT_PATH
        
        self.change_y_aim = 0
        self.change_x_aim = 12

        #Cada frame es de 64x64
        WIDTH = 64
        HEIGHT = 64

        # Astronauta: Caminar: 4 frames en cuadrícula 2x2
        self.walk_forward, self.walk_forward_flipped = load_spritesheet_pair(str(ruta_base / "astronaut_walk_forward_3.0.png"), 4, WIDTH, HEIGHT, 2)
        self.walk_up, self.walk_up_flipped = load_spritesheet_pair(str(ruta_base / "astronaut_walk_up_3.0.png"), 4, WIDTH, HEIGHT, 2)
        self.walk_down, self.walk_down_flipped = load_spritesheet_pair(str(ruta_base / "astronaut_walk_down_3.0.png"), 4, WIDTH, HEIGHT, 2)
        self.walk_forward_up, self.walk_forward_up_flipped = load_spritesheet_pair(str(ruta_base / "astronaut_walk_forward_up_2.0.png"), 4, WIDTH, HEIGHT, 2)
        self.walk_forward_down, self.walk_forward_down_flipped = load_spritesheet_pair(str(ruta_base / "astronaut_walk_forward_down_2.0.png"), 4, WIDTH, HEIGHT, 2)

        #Astronauta: Saltar: 1 solo frame
        self.jump_forward, self.jump_forward_flipped = load_spritesheet_pair(str(ruta_base / "astronaut_jump_forward_3.0.png"), 1, WIDTH, HEIGHT, 1)
        self.jump_up, self.jump_up_flipped = load_spritesheet_pair(str(ruta_base / "astronaut_jump_up_3.0.png"), 1, WIDTH, HEIGHT, 1)
        self.jump_down, self.jump_down_flipped = load_spritesheet_pair(str(ruta_base / "astronaut_jump_down_2.0.png"), 1, WIDTH, HEIGHT, 1)
        self.jump_forward_up, self.jump_forward_up_flipped = load_spritesheet_pair(str(ruta_base / "astronaut_jump_forward_up_2.0.png"), 1, WIDTH, HEIGHT, 1)
        self.jump_forward_down, self.jump_forward_down_flipped = load_spritesheet_pair(str(ruta_base / "astronaut_jump_forward_down_2.0.png"), 1, WIDTH, HEIGHT, 1)
        
        #Textura del astronauta por defecto
        self.texture = self.walk_forward[1]

    def update_animation(self, delta_time):
        #Dirección horizontal
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        #Dirección vertical
        if self.change_y_aim > 0 and self.change_x_aim != 0:
            self.vertical_facing = FACE_UP_DIAGONAL  #apunta 45º
        elif self.change_y_aim > 0 and self.change_x_aim == 0:
            self.vertical_facing = FACE_UP           #apunta recto arriba
        elif self.change_y_aim < 0 and self.change_x_aim != 0:
            self.vertical_facing = FACE_DOWN_DIAGONAL
        elif self.change_y_aim < 0 and self.change_x_aim == 0:
            self.vertical_facing = FACE_DOWN
        else:
            self.vertical_facing = FACE_FORWARD

        #Variables auxiliares para facilitar la lectura
        mirando_izquierda = self.facing_direction == LEFT_FACING
        esta_moviendose = self.change_x != 0

        #Elegir animación correcta
        if not self.is_on_ground:
            #Animaciones de salto
            if self.vertical_facing == FACE_UP_DIAGONAL or self.vertical_facing == FACE_UP:
                texturas = self.jump_forward_up_flipped if mirando_izquierda else self.jump_forward_up
            elif self.vertical_facing == FACE_DOWN_DIAGONAL or self.vertical_facing == FACE_DOWN:
                texturas = self.jump_forward_down_flipped if mirando_izquierda else self.jump_forward_down
            else:
                texturas = self.jump_forward_flipped if mirando_izquierda else self.jump_forward

        else:
            #Animaciones de caminar o quieto
            if self.vertical_facing == FACE_UP_DIAGONAL:
                if esta_moviendose:
                    texturas = self.walk_forward_up_flipped if mirando_izquierda else self.walk_forward_up
                else:
                    self.cur_texture = 0
                    self.texture = self.walk_forward_up_flipped[1] if mirando_izquierda else self.walk_forward_up[1]
                    return
            elif self.vertical_facing == FACE_UP:
                if esta_moviendose:
                    texturas = self.walk_up_flipped if mirando_izquierda else self.walk_up
                else:
                    self.cur_texture = 0
                    self.texture = self.walk_up_flipped[1] if mirando_izquierda else self.walk_up[1]
                    return
            elif self.vertical_facing == FACE_DOWN_DIAGONAL:
                if esta_moviendose:
                    texturas = self.walk_forward_down_flipped if mirando_izquierda else self.walk_forward_down
                else:
                    self.cur_texture = 0
                    self.texture = self.walk_forward_down_flipped[1] if mirando_izquierda else self.walk_forward_down[1]
                    return
            elif self.vertical_facing == FACE_DOWN:
                if esta_moviendose:
                    texturas = self.walk_down_flipped if mirando_izquierda else self.walk_down
                else:
                    self.cur_texture = 0
                    self.texture = self.walk_down_flipped[1] if mirando_izquierda else self.walk_down[1]
                    return
            else:
                if esta_moviendose:
                    texturas = self.walk_forward_flipped if mirando_izquierda else self.walk_forward
                else:
                    self.cur_texture = 0
                    self.texture = self.walk_forward_flipped[1] if mirando_izquierda else self.walk_forward[1]
                    return
                
        #Avanzar al siguiente frame de animación
        self.cur_texture += 1
        if self.cur_texture >= len(texturas) * UPDATES_PER_FRAME:
            self.cur_texture = 0

        self.texture = texturas[self.cur_texture // UPDATES_PER_FRAME]

class Enemy(Character):
    def __init__(self, name_folder, name_file):
        super().__init__(name_folder, name_file)

        #Cada frame es de 64x64
        WIDTH = 64
        HEIGHT = 64

        self.should_update_walk = 0

    def update_animation(self, delta_time):
        # Figure out the direction the character is facing based on the
        # movement and previous direction.
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Handle idle animations
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Handle walking
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1


class RobotEnemy(Enemy):
    def __init__(self):
        super().__init__("robot", "robot")
        self.health = 100


class ZombieEnemy(Enemy):
    def __init__(self):
        super().__init__("zombie", "zombie")
        self.health = 50

        WIDTH = 64
        HEIGHT = 64

        ruta_base = ZOMBIE_PATH

        #Zombie: Caminar
        self.zombie_walk_forward, self.zombie_walk_forward_flipped = load_spritesheet_pair(str(ruta_base / "zombie_walk_forward_2.0.png"), 1, WIDTH, HEIGHT, 1)
        self.zombie_jump_forward_up, self.zombie_jump_forward_up_flipped = load_spritesheet_pair(str(ruta_base / "zombie_jump_forward_up_2.0.png"), 1, WIDTH, HEIGHT, 1)
        self.zombie_jump_forward_down, self.zombie_jump_forward_down_flipped = load_spritesheet_pair(str(ruta_base / "zombie_jump_forward_down_2.0.png"), 1, WIDTH, HEIGHT, 1)