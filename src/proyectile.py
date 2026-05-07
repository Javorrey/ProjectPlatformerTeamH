import math
from pathlib import Path
import arcade
from constants import *

class ProyectilBase(arcade.Sprite):
    def __init__(self, pos_x, pos_y, vel_x, vel_y, imagen, escala, dmg):
        super().__init__(imagen, scaling=escala)
        
        # Posición inicial (la del jugador)
        self.center_x = pos_x
        self.center_y = pos_y
        
        # Velocidad y dirección
        self.change_x = vel_x
        self.change_y = vel_y
        
        # Atributos personalizados
        self.dmg = dmg

        # ¡La rotación automática se hace aquí al nacer!
        angulo_radianes = math.atan2(self.change_y, self.change_x)
        self.angle = -math.degrees(angulo_radianes)

    def update(self, *args, **kwargs):
        # Si más adelante quieres balas que caigan con gravedad 
        # o que persigan al jugador, la lógica iría aquí.
        super().update(*args, **kwargs)

        

class LaserAzul(ProyectilBase):
    def __init__(self, pos_x, pos_y, vel_x, vel_y):
        # Le pasamos la imagen, la escala (0.8) y el daño (25)
        super().__init__(
            pos_x, pos_y, vel_x, vel_y, 
            ":resources:images/space_shooter/laserBlue01.png", 
            0.8, 
            25
        )

class ProyectilExplosivo(ProyectilBase):
    def __init__(self, pos_x, pos_y, vel_x, vel_y):
        # Una bola de fuego más grande, más lenta, pero que hace más daño (50)
        super().__init__(
            pos_x, pos_y, vel_x * 0.5, vel_y * 0.5, # Mitad de velocidad
            ":resources:images/space_shooter/meteorGrey_small1.png", 
            1.2, 
            50
        )