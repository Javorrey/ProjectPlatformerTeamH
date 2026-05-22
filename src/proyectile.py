import math
from pathlib import Path
import arcade
from constants import *

class ProyectilBase(arcade.Sprite):
    def __init__(self, pos_x, pos_y, vel_x, vel_y, imagen, escala, dmg, juego):
        super().__init__(imagen, scaling=escala)
        
        # Posición inicial (la del jugador)
        self.center_x = pos_x
        self.center_y = pos_y
        
        # Velocidad y dirección
        self.change_x = vel_x
        self.change_y = vel_y
        self.dmg = dmg

        self.juego = juego  


        angulo_radianes = math.atan2(self.change_y, self.change_x)
        self.angle = -math.degrees(angulo_radianes)

    def update(self, *args, **kwargs):
        # Si más adelante quieres balas que caigan con gravedad 
        # o que persigan al jugador, la lógica iría aquí.
        super().update(*args, **kwargs)
        self.comprobar_colisiones()

    def comprobar_colisiones(self):
        hit_list = arcade.check_for_collision_with_lists(
            self,
            [
                self.juego.scene["Enemies"],
                self.juego.scene["walls"],
                self.juego.scene["Platforms"],
                self.juego.scene["Moving_Platforms"],
                self.juego.scene["Paredes_Destructibles"]
                
            ]
        )

        if hit_list:
            for collision in hit_list:
                if self.juego.scene["Enemies"] in collision.sprite_lists:
                    collision.health -= self.dmg
                    if collision.health <= 0:
                        collision.remove_from_sprite_lists()
                        self.juego.score += 150 # Sumamos puntos a la partida
                elif self.juego.scene["Paredes_Destructibles"] in collision.sprite_lists:
                    if hasattr(collision, "health"):
                        collision.health -= self.dmg
                        if collision.health <= 0 :
                            collision.remove_from_sprite_lists()


            self.remove_from_sprite_lists()
            arcade.play_sound(self.juego.hit_sound)

        # Destruir si sale del mapa
        if (self.right < 0) or (self.left > self.juego.end_of_map):
            self.remove_from_sprite_lists()

        

class LaserAzul(ProyectilBase):
    def __init__(self, pos_x, pos_y, vel_x, vel_y, juego):
        super().__init__(
            pos_x, pos_y, vel_x, vel_y, 
            ":resources:images/space_shooter/laserBlue01.png", 
            0.8, 
            25, 
            juego
        )


class ProyectilExplosivo(ProyectilBase):
    def __init__(self, pos_x, pos_y, vel_x, vel_y, juego):
        # Una bola de fuego más grande, más lenta, pero que hace más daño (50)
        super().__init__(
            pos_x, pos_y, vel_x * 0.5, vel_y * 0.5, # Mitad de velocidad
            ":resources:images/space_shooter/meteorGrey_small1.png", 
            1.2, 
            50,
            juego
        )
        self.radio_explosion = 150

    # Sobrescribimos las colisiones solo para el explosivo
    def comprobar_colisiones(self):
        hit_list = arcade.check_for_collision_with_lists(
            self,
            [
                self.juego.scene["Enemies"],
                self.juego.scene["walls"],
                self.juego.scene["Platforms"],
                self.juego.scene["Paredes_Destructibles"]

            ]
        )

        if hit_list:
            # 1. Rocket Jump al jugador
            dist_jugador = arcade.get_distance_between_sprites(self, self.juego.player_sprite)
            if dist_jugador <= self.radio_explosion:
                dx = self.juego.player_sprite.center_x - self.center_x
                dy = self.juego.player_sprite.center_y - self.center_y
                angulo_empuje = math.atan2(dy, dx)
                fuerza = 28 
                #self.juego.player_sprite.change_x += math.cos(angulo_empuje) * fuerza/3
                self.juego.player_sprite.change_y += math.sin(angulo_empuje) * fuerza

            # 2. Daño a enemigos en área
            for enemy in self.juego.scene["Enemies"]:
                distancia = arcade.get_distance_between_sprites(self, enemy)
                if distancia <= self.radio_explosion:
                    enemy.health -= self.dmg
                    if enemy.health <= 0:
                        enemy.remove_from_sprite_lists()
                        self.juego.score += 150
                
            for bloque in self.juego.scene["Paredes_Destructibles"]:
                distancia_pared = arcade.get_distance_between_sprites(self, bloque)
                if distancia_pared <= self.radio_explosion:
                    bloque.health -= self.dmg  # Quita 50 de daño (el misil la rompe de 1 tiro)
                    if bloque.health <= 0:
                        bloque.remove_from_sprite_lists()
                        self.juego.score += 50
            
            self.remove_from_sprite_lists()
            arcade.play_sound(self.juego.hit_sound)


class DisparoPrincipal(arcade.Sprite):
    def __init__(self, pos_x, pos_y, vel_x, vel_y, juego):
        super().__init__()
        self.center_x = pos_x
        self.center_y = pos_y
        self.change_x = vel_x
        self.change_y = vel_y
        self.dmg = 25
        self.juego = juego

        self.path_or_texture = str(PROJECTILE_PATH / "Friendly Fire 2.0.png")
        self.texture_sheet = arcade.load_spritesheet(self.path_or_texture)
        self.texture_list = self.texture_sheet.get_texture_grid(
            size=(64, 64),  
            columns=2,      
            count=5         
        )
        #print(len(self.texture_list))

        self.texture = self.texture_list[0]

        self.animation_speed = 0.1
        self.impact = False
        self.animation_frame = 0
        self.accumulatedTime = 0.0

        angulo_radianes = math.atan2(self.change_y, self.change_x)
        self.angle = -math.degrees(angulo_radianes)

    def update(self, delta_time: float, *args, **kwargs):
        if not self.impact:
            super().update(*args, **kwargs)
            self.check_collisions()

            if (self.right < 0) or (self.left > self.juego.end_of_map):
                self.remove_from_sprite_lists()
            if (self.bottom < 0) or (self.top > self.juego.tile_map.height * self.juego.tile_map.tile_height):
                self.remove_from_sprite_lists()

        else:
            self.accumulatedTime += delta_time
            

            if self.accumulatedTime >= self.animation_speed:
                self.accumulatedTime = 0.0
                self.animation_frame += 1

                if self.animation_frame < len(self.texture_list):
                    self.texture = self.texture_list[self.animation_frame]
                else:
                    self.remove_from_sprite_lists()

    def check_collisions(self):
        if self.impact:
            return
        hit_list = arcade.check_for_collision_with_lists(
            self,
            [
                self.juego.scene["Enemies"],
                self.juego.scene["walls"],
                self.juego.scene["Platforms"],
                self.juego.scene["Moving_Platforms"],
                self.juego.scene["Paredes_Destructibles"]
                
            ]
        )
        if hit_list:
            for collision in hit_list:
                if self.juego.scene["Enemies"] in collision.sprite_lists:
                    collision.health -= self.dmg
                    if collision.health <= 0:
                        collision.remove_from_sprite_lists()
                        self.juego.score += 150 # Sumamos puntos a la partida
                elif self.juego.scene["Paredes_Destructibles"] in collision.sprite_lists:
                    if hasattr(collision, "health"):
                        collision.health -= self.dmg
                        if collision.health <= 0 :
                            collision.remove_from_sprite_lists()
                            self.juego.score += 50
            
            self.change_x = 0
            self.change_y = 0
            self.impact = True
            arcade.play_sound(self.juego.hit_sound)
            self.animation_frame = 0
            self.texture = self.texture_list[self.animation_frame]

class DisparoSecundario(DisparoPrincipal):
    def __init__(self, pos_x, pos_y, vel_x, vel_y, juego):
        super().__init__(pos_x, pos_y, vel_x * 0.5, vel_y * 0.5, juego)
        self.dmg = 50
        self.path_or_texture = str(PROJECTILE_PATH / "Friendly Fire 2.0.png")
        self.texture_sheet = arcade.load_spritesheet(self.path_or_texture)
        self.texture_list = self.texture_sheet.get_texture_grid(
            size=(64, 64),  
            columns=2,      
            count=5         
        )
        self.texture = self.texture_list[0]
        self.animation_speed = 0.1
        self.impact = False
        self.animation_frame = 0
        self.accumulatedTime = 0.0

        angulo_radianes = math.atan2(self.change_y, self.change_x)
        self.angle = -math.degrees(angulo_radianes)

        self.radio_explosion = 150

        def check_collisions(self):
            if self.impact:
                return
            hit_list = arcade.check_for_collision_with_lists(
                self,
                [
                    self.juego.scene["Enemies"],
                    self.juego.scene["walls"],
                    self.juego.scene["Platforms"],
                    self.juego.scene["Moving_Platforms"],
                    self.juego.scene["Paredes_Destructibles"]
                    
                ]
            )
            if hit_list:
                # 1. Rocket Jump al jugador
                dist_jugador = arcade.get_distance_between_sprites(self, self.juego.player_sprite)
                if dist_jugador <= self.radio_explosion:
                    dx = self.juego.player_sprite.center_x - self.center_x
                    dy = self.juego.player_sprite.center_y - self.center_y
                    angulo_empuje = math.atan2(dy, dx)
                    fuerza = 28 
                    #self.juego.player_sprite.change_x += math.cos(angulo_empuje) * fuerza/3
                    self.juego.player_sprite.change_y += math.sin(angulo_empuje) * fuerza

                # 2. Daño a enemigos en área
                for enemy in self.juego.scene["Enemies"]:
                    distancia = arcade.get_distance_between_sprites(self, enemy)
                    if distancia <= self.radio_explosion:
                        enemy.health -= self.dmg
                        if enemy.health <= 0:
                            enemy.remove_from_sprite_lists()
                            self.juego.score += 150
                    
                for bloque in self.juego.scene["Paredes_Destructibles"]:
                    distancia_pared = arcade.get_distance_between_sprites(self, bloque)
                    if distancia_pared <= self.radio_explosion:
                        bloque.health -= self.dmg  # Quita 50 de daño (el misil la rompe de 1 tiro)
                        if bloque.health <= 0:
                            bloque.remove_from_sprite_lists()
                            self.juego.score += 50
                
                self.change_x = 0
                self.change_y = 0
                self.impact = True
                arcade.play_sound(self.juego.hit_sound)
                self.animation_frame = 0
                self.texture = self.texture_list[self.animation_frame]

