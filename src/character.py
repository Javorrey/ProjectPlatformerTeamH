import math
from pathlib import Path
import arcade
from proyectile import *
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

        self.shoot_timer = 0

        WIDTH = 64
        HEIGHT = 64

        ruta_base = ALIEN_PATH

        #Alien andando y saltando
        self.alien_walk, self.alien_walk_flipped = load_spritesheet_pair(str(ruta_base / "alien_walk_3.0.png"), 4, WIDTH, HEIGHT, 2)
        self.alien_jump, self.alien_jump_flipped = load_spritesheet_pair(str(ruta_base / "alien_jump_2.0.png"), 4, WIDTH, HEIGHT, 2)

        #Textura inicial por defecto
        self.texture = self.alien_walk[0]
        
    def update_animation(self, delta_time): 
        super().update_animation(delta_time)
        
        #Variables auxiliares para facilitar la lectura
        mirando_izquierda = self.facing_direction == LEFT_FACING
        
        #Elegir animación correcta
        if self.change_y != 0:
            #Si se está moviendo en vertical, usamos la animación de salto
            texturas = self.alien_jump_flipped if mirando_izquierda else self.alien_jump
        elif self.change_x != 0:
            #Si se mueve solo en horizontal, usamos la animación de caminar
            texturas = self.alien_walk_flipped if mirando_izquierda else self.alien_walk
        else:
            #Si está completamente quieto 
            texturas = self.alien_walk_flipped if mirando_izquierda else self.alien_walk
            self.cur_texture = 0
            self.texture = texturas[0] # Usamos el primer frame como pose Idle
            return
            
        #Avanzar al siguiente frame de animación
        self.cur_texture += 1

        #Si llegamos al final de la animación, volvemos a empezar
        if self.cur_texture >= len(texturas) * UPDATES_PER_FRAME:
            self.cur_texture = 0
            
        #Asignamos la textura correspondiente calculando el frame actual
        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = texturas[frame]

    def update(self, delta_time):
        #Comprobamos si tiene el juego conectado
        if not hasattr(self, "juego") or not self.juego.player_sprite:
            return

        jugador = self.juego.player_sprite

        #Calculamos la distancia entre el brain alien y el jugador
        distancia = arcade.get_distance_between_sprites(self, jugador)

        #LÓGICA DE DISPARO
        #Modo ofensivo: detenerse y disparar
        if distancia < ALIEN_VISION_RANGE:
            self.change_x = 0
            self.change_y = 0

            if jugador.center_x < self.center_x:
                self.facing_direction = LEFT_FACING
            else:
                self.facing_direction = RIGHT_FACING

            self.shoot_timer += 1
            if self.shoot_timer >= ALIEN_FIRE_RATE:
                self.shoot_timer = 0
                self.disparar(jugador)
        else:
            #Modo pasivo: patrulla
            self.shoot_timer = 0 
            self.change_y = 0    

            if self.change_x == 0:
                self.change_x = ALIEN_PATROL_SPEED
            elif self.change_x > 0:
                self.change_x = ALIEN_PATROL_SPEED
            elif self.change_x < 0:
                self.change_x = -ALIEN_PATROL_SPEED

        super().update()

    def disparar(self, jugador):
        """Calcula el ángulo hacia el jugador y crea una bala"""

        dx = jugador.center_x - self.center_x
        dy = jugador.center_y - self.center_y
        angulo = math.atan2(dy, dx)

        vel_x = math.cos(angulo) * ALIEN_BULLET_SPEED
        vel_y = math.sin(angulo) * ALIEN_BULLET_SPEED

        bala_enemiga = AlienProyectile(self.center_x, self.center_y, vel_x, vel_y, self.juego)
        bala_enemiga.angle = math.degrees(angulo) 

        self.juego.scene.add_sprite("Balas_Enemigas", bala_enemiga)

class ZombieEnemy(Enemy):
    def __init__(self):
        super().__init__()
        
        self.health = 50
        self.patrol_flip_cooldown = 0  # 

        WIDTH = 64
        HEIGHT = 64

        ruta_base = ZOMBIE_PATH

        #Texturas del zombie
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

    def update(self, delta_time):
        #Comprobamos si tiene el juego conectado
        if not hasattr(self, "juego") or not self.juego.player_sprite:
            return
        #Guardamos donde nace el zombie
        if not hasattr(self, "posicion_inicial_x"):
            self.posicion_inicial_x = self.center_x
            self.rango_patrulla = 45
        
        jugador = self.juego.player_sprite
        #Calculamos la distancia entre el jugador y el zombie
        distancia = arcade.get_distance_between_sprites(self, jugador)

        #LÓGICA DE PERSECUCIÓN
        #Modo persecución
        if distancia < ZOMBIE_VISION_RANGE:
            if jugador.center_x > self.center_x:
                self.change_x = ZOMBIE_CHASE_SPEED
            elif jugador.center_x < self.center_x:
                self.change_x = -ZOMBIE_CHASE_SPEED
        else:
            # Modo patrulla
            if self.change_x == 0:
                self.change_x = ZOMBIE_PATROL_SPEED

        super().update()
        self.comprobar_colisiones()

    def comprobar_colisiones(self):
        
        #Colisión con los pinchos
        pinchos_tocados = arcade.check_for_collision_with_list(self, self.juego.scene["Daño"])
        if pinchos_tocados:
            #El zombi muere al pisar la trampa!
            self.remove_from_sprite_lists()
            return 

        #Colisión con el escenario (Paredes, plataformas, etc)
        listas_escenario = [
            self.juego.scene["walls"],
            self.juego.scene["Platforms"],
            self.juego.scene["Paredes_Destructibles"]
        ]
        obstaculos_tocados = arcade.check_for_collision_with_lists(self, listas_escenario)


        # Revisamos todos los obstáculos que está tocando
        for muro in obstaculos_tocados:
            #Si el obstáculo está por debajo de sus pies, es el suelo
            if self.bottom >= muro.top - 10:
                continue # Pasa al siguiente obstáculo sin hacer nada
            #Muro real: rebotar
            if self.change_x > 0: 
                self.right = muro.left 
                self.change_x = -ZOMBIE_PATROL_SPEED 
            elif self.change_x < 0: 
                self.left = muro.right 
                self.change_x = ZOMBIE_PATROL_SPEED 
                
            self.posicion_inicial_x = self.center_x
            
            #Rompemos el bucle porque ya hemos rebotado
            break
        