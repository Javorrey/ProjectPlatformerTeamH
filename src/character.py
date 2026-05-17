import math
from pathlib import Path
import arcade
from constants import *
from PIL import Image

#Constantes de dirección 
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

class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__()

        #Cada frame es de 64x64
        WIDTH = 64
        HEIGHT = 64

        self.cur_texture = 0
        self.should_update_walk = 0

        self.facing_direction = RIGHT_FACING
        self.vertical_facing = FACE_FORWARD


    def update_animation(self, delta_time):
        # Figure out the direction the character is facing based on the
        # movement and previous direction.
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        


class AlienEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 100

        WIDTH = 64
        HEIGHT = 64

        ruta_base = ALIEN_PATH

        #Alien: Caminar
        self.alien_walk_forward, self.alien_walk_forward_flipped = load_spritesheet_pair(str(ruta_base / "alien_walk_forward_2.0.png"), 1, WIDTH, HEIGHT, 1)
        self.alien_walk_forward_up, self.alien_walk_forward_up_flipped = load_spritesheet_pair(str(ruta_base / "alien_walk_forward_up_2.0.png"), 1, WIDTH, HEIGHT, 1)
        self.alien_walk_forward_down, self.alien_walk_forward_down_flipped = load_spritesheet_pair(str(ruta_base / "alien_walk_forward_down_2.0.png"), 1, WIDTH, HEIGHT, 1)
        
    def update_animation(self, delta_time): 
        super().update_animation(delta_time)
        #Variables auxiliares para facilitar la lectura
        mirando_izquierda = self.facing_direction == LEFT_FACING
        esta_moviendose = self.change_x != 0

        #Animaciones de caminar o quieto
        if self.vertical_facing == FACE_UP_DIAGONAL:
            if esta_moviendose:
                texturas = self.alien_walk_forward_up_flipped if mirando_izquierda else self.alien_walk_forward_up
            else:
                self.cur_texture = 0
                self.texture = self.alien_walk_forward_up_flipped[1] if mirando_izquierda else self.alien_walk_forward_up[1]
                return
        elif self.vertical_facing == FACE_UP:
            if esta_moviendose:
                texturas = self.alien_jump_forward_up_flipped if mirando_izquierda else self.alien_jump_forward_up
            else:
                self.cur_texture = 0
                self.texture = self.alien_jump_forward_up_flipped[1] if mirando_izquierda else self.alien_jump_forward_up[1]
                return
        elif self.vertical_facing == FACE_DOWN_DIAGONAL:
            if esta_moviendose:
                texturas = self.alien_jump_forward_down_flipped if mirando_izquierda else self.alien_jump_forward_down
            else:
                self.cur_texture = 0
                self.texture = self.alien_jump_forward_down_flipped[1] if mirando_izquierda else self.alien_jump_forward_down[1]
                return
        elif self.vertical_facing == FACE_DOWN:
            if esta_moviendose:
                texturas = self.alien_jump_forward_down_flipped if mirando_izquierda else self.alien_jump_forward_down
            else:
                self.cur_texture = 0
                self.texture = self.alien_jump_forward_down_flipped[1] if mirando_izquierda else self.alien_jump_forward_down[1]
                return
        else:
            if esta_moviendose:
                texturas = self.alien_walk_forward_flipped if mirando_izquierda else self.alien_walk_forward
            else:
                self.cur_texture = 0
                self.texture = self.alien_walk_forward_flipped[1] if mirando_izquierda else self.alien_walk_forward[1]
                return
            
        #Avanzar al siguiente frame de animación
        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = texturas[frame]
        self.cur_texture += 1
        if self.cur_texture >= len(texturas) * UPDATES_PER_FRAME:
            self.cur_texture = 0
        


class ZombieEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 50

        WIDTH = 64
        HEIGHT = 64

        ruta_base = ZOMBIE_PATH

        #Zombie: Caminar
        self.zombie_walk_forward, self.zombie_walk_forward_flipped = load_spritesheet_pair(str(ruta_base / "zombie_walk_forward_2.0.png"), 1, WIDTH, HEIGHT, 1)
        self.zombie_walk_forward_up, self.zombie_walk_forward_up_flipped = load_spritesheet_pair(str(ruta_base / "zombie_walk_forward_up_2.0.png"), 1, WIDTH, HEIGHT, 1)
        self.zombie_walk_forward_down, self.zombie_walk_forward_down_flipped = load_spritesheet_pair(str(ruta_base / "zombie_walk_forward_down_2.0.png"), 1, WIDTH, HEIGHT, 1)

    def update_animation(self, delta_time):
        super().update_animation(delta_time)
        #Variables auxiliares para facilitar la lectura
        mirando_izquierda = self.facing_direction == LEFT_FACING
        esta_moviendose = self.change_x != 0

        #Animaciones de caminar o quieto
        if self.vertical_facing == FACE_UP_DIAGONAL:
            if esta_moviendose:
                texturas = self.zombie_walk_forward_up_flipped if mirando_izquierda else self.zombie_walk_forward_up
            else:
                self.cur_texture = 0
                self.texture = self.zombie_walk_forward_up_flipped[1] if mirando_izquierda else self.zombie_walk_forward_up[1]
                return
        elif self.vertical_facing == FACE_UP:
            if esta_moviendose:
                texturas = self.zombie_walk_forward_up_flipped if mirando_izquierda else self.zombie_walk_forward_up
            else:
                self.cur_texture = 0
                self.texture = self.zombie_walk_forward_up_flipped[1] if mirando_izquierda else self.zombie_walk_forward_up[1]
                return
        elif self.vertical_facing == FACE_DOWN_DIAGONAL:
            if esta_moviendose:
                texturas = self.zombie_walk_forward_down_flipped if mirando_izquierda else self.zombie_walk_forward_down
            else:
                self.cur_texture = 0
                self.texture = self.zombie_walk_forward_down_flipped[1] if mirando_izquierda else self.zombie_walk_forward_down[1]
                return
        elif self.vertical_facing == FACE_DOWN:
            if esta_moviendose:
                texturas = self.zombie_walk_forward_down_flipped if mirando_izquierda else self.zombie_walk_forward_down
            else:
                self.cur_texture = 0
                self.texture = self.zombie_walk_forward_down_flipped[1] if mirando_izquierda else self.zombie_walk_forward_down[1]
                return
        else:
            if esta_moviendose:
                texturas = self.zombie_walk_forward_flipped if mirando_izquierda else self.zombie_walk_forward
            else:
                self.cur_texture = 0
                self.texture = self.zombie_walk_forward_flipped[1] if mirando_izquierda else self.zombie_walk_forward[1]
                return
        #Avanzar al siguiente frame de animación
        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = texturas[frame]
        self.cur_texture += 1
        if self.cur_texture >= len(texturas) * UPDATES_PER_FRAME:
            self.cur_texture = 0