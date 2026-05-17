import arcade

from niveles import VistaNiveles
from ajustes import VistaAjustes

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from constants import *

class mainMenu(arcade.View):
    def __init__(self):
        """
        Inicializamos la vista y cargamos todos los recursos
        """
        super().__init__()

        arcade.load_font(str(BASE_DIR / "assets" / "fonts" / "fuente_menu.ttf"))
        
        self.fondo = arcade.load_texture(str(BASE_DIR / "assets" / "images" / "menu" / "main" / "fondo_menu.png"))

        self.lista_botones = arcade.SpriteList()
        
        self.boton_jugar = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "main" / "boton_jugar_menu.png"), scale = 1.8)
        self.boton_nivel = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "main" / "boton_nivel_menu.png"), scale = 1.8)
        self.boton_ajustes = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "main" / "boton_ajustes_menu.png"), scale = 1.8)
        self.boton_salir = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "main" / "boton_salir_menu.png"), scale = 1.8)

        self.lista_botones.append(self.boton_jugar)
        self.lista_botones.append(self.boton_nivel)
        self.lista_botones.append(self.boton_ajustes)
        self.lista_botones.append(self.boton_salir)

    def on_show_view(self):
        centro_x = self.window.width / 2
        alto = self.window.height

        self.boton_jugar.center_x = centro_x
        self.boton_jugar.center_y = alto * (340/600)

        self.boton_nivel.center_x = centro_x
        self.boton_nivel.center_y = alto * (270/600)

        self.boton_ajustes.center_x = centro_x
        self.boton_ajustes.center_y = alto * (200/600)

        self.boton_salir.center_x = centro_x
        self.boton_salir.center_y = alto * (130/600)

    def on_draw(self):
        self.clear()
        
        centro_x = self.window.width / 2

        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, self.window.width, self.window.height))

        self.lista_botones.draw()

        texto_nivel = f"Nivel seleccionado: {self.window.nivel_seleccionado}"
        texto_nivel_x = 150
        texto_nivel_y = 50
        arcade.draw_text(texto_nivel, texto_nivel_x, texto_nivel_y, color=arcade.color.WHITE, font_size=15, font_name="Upheaval TT (BRK)", anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Lógica para detectar clics y cambiar de vista
        """
        botones_pulsados = arcade.get_sprites_at_point((x, y), self.lista_botones)

        if len(botones_pulsados) > 0:
            boton_clicado = botones_pulsados[0]

            #Cuando se hagan los niveles se termina esto
            if boton_clicado == self.boton_jugar:
                pass
                """
                if self.window.nivel_seleccionado == 1:
                    vista_juego = 
                    self.window.show_view(vista_juego)

                if self.window.nivel_seleccionado == 2:
                    vista_juego = 
                    self.window.show_view(vista_juego)

                if self.window.nivel_seleccionado == 3:
                    vista_juego = 
                    self.window.show_view(vista_juego)

                if self.window.nivel_seleccionado == 4:
                    vista_juego = 
                    self.window.show_view(vista_juego)

                if self.window.nivel_seleccionado == 5:
                    vista_juego = 
                    self.window.show_view(vista_juego)"""

            if boton_clicado == self.boton_nivel:
                proxima_vista = VistaNiveles()
                self.window.show_view(proxima_vista)

            elif boton_clicado == self.boton_ajustes:
                proxima_vista = VistaAjustes()
                self.window.show_view(proxima_vista)

            elif boton_clicado == self.boton_salir:
                arcade.exit()

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

if __name__ == '__main__':
    ventana = arcade.Window(800, 600, "Artemis 67")
    
    #Registramos la ventana
    ventana.MainMenuClass = mainMenu

    ventana.nivel_seleccionado = 1
    
    #ventana.volumen_seleccionado = 0.7  terminar cuando elijamos musica

    vista_menu = mainMenu()
    ventana.show_view(vista_menu)
    arcade.run()
