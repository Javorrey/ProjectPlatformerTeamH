import arcade

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from constants import *

class VistaNiveles(arcade.View):
    def __init__(self):
        """
        Inicializamos la vista y cargamos todos los recursos
        """
        super().__init__()

        self.fondo = arcade.load_texture("assets/images/menu/nivel/fondo_menu.png")

        self.lista_botones = arcade.SpriteList()
        
        self.boton_nivel1 = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "nivel" / "boton_nivel1_menu.png"), scale = 1.8)
        self.boton_nivel2 = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "nivel" / "boton_nivel2_menu.png"), scale = 1.8)
        self.boton_nivel3 = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "nivel" / "boton_nivel3_menu.png"), scale = 1.8)
        self.boton_nivel4 = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "nivel" / "boton_nivel4_menu.png"), scale = 1.8)
        self.boton_nivel5 = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "nivel" / "boton_nivel5_menu.png"), scale = 1.8)

        self.boton_atras = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "nivel" / "flecha_atras_menu.png"), scale = 1.8)

        self.lista_botones.append(self.boton_nivel1)
        self.lista_botones.append(self.boton_nivel2)
        self.lista_botones.append(self.boton_nivel3)
        self.lista_botones.append(self.boton_nivel4)
        self.lista_botones.append(self.boton_nivel5)
        self.lista_botones.append(self.boton_atras)
        
    def on_show_view(self):
        centro_x = self.window.width / 2
        alto = self.window.height 

        self.boton_nivel1.center_x = centro_x
        self.boton_nivel1.center_y = alto * (370/600)

        self.boton_nivel2.center_x = centro_x
        self.boton_nivel2.center_y = alto * (300/600)

        self.boton_nivel3.center_x = centro_x
        self.boton_nivel3.center_y = alto * (230/600)

        self.boton_nivel4.center_x = centro_x
        self.boton_nivel4.center_y = alto * (160/600)

        self.boton_nivel5.center_x = centro_x
        self.boton_nivel5.center_y = alto * (90/600)
        
        self.boton_atras.center_x = 50
        self.boton_atras.center_y = alto - 50
    
    def on_draw(self):
        self.clear()
        
        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, self.window.width, self.window.height))

        self.lista_botones.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Lógica para detectar clics y cambiar de vista
        """
        botones_pulsados = arcade.get_sprites_at_point((x, y), self.lista_botones)

        if len(botones_pulsados) > 0:
            boton_clicado = botones_pulsados[0]

            if boton_clicado == self.boton_nivel1:
                self.window.nivel_seleccionado = 1

            elif boton_clicado == self.boton_nivel2:
                self.window.nivel_seleccionado = 2

            elif boton_clicado == self.boton_nivel3:
                self.window.nivel_seleccionado = 3

            elif boton_clicado == self.boton_nivel4:
                self.window.nivel_seleccionado = 4

            elif boton_clicado == self.boton_nivel5:
                self.window.nivel_seleccionado = 5

            elif boton_clicado == self.boton_atras:
                proxima_vista = self.window.MainMenuClass()
                self.window.show_view(proxima_vista)
            
    
    def on_mouse_motion(self, x, y, dx, dy):
        """
        Función para añadir efectos cuando se pasa la flecha del ratón por encima de los botones
        """
        #Reseteo
        for boton in self.lista_botones:
            boton.scale = 1.8
        
        #Detección
        botones_tocados = arcade.get_sprites_at_point((x, y), self.lista_botones)

        #Efecto
        if len(botones_tocados) > 0:
            boton_actual = botones_tocados[0]
            boton_actual.scale = 2.0

    def on_resize(self, width, height):
        """ 
        Se ejecuta automáticamente al cambiar el tamaño de la ventana o poner pantalla completa 
        """
        super().on_resize(width, height)
        
        #Le decimos al botón de Atrás que calcule su nueva posición en el techo
        self.boton_atras.center_x = 50
        self.boton_atras.center_y = height - 50

    
if __name__ == '__main__':
    ventana = arcade.Window(800, 600, "Artemis 67")
    vista_nivel = VistaNiveles()
    ventana.show_view(vista_nivel)
    arcade.run()