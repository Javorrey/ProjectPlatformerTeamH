import arcade

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from constants import *

class VistaControles(arcade.View):
    def __init__(self):
        """
        Inicializamos la vista y cargamos todos los recursos
        """
        super().__init__()

        self.fondo = arcade.load_texture(str(BASE_DIR / "assets" / "images" / "menu" / "controles"/ "fondo_menu.png"))

        self.lista_botones = arcade.SpriteList()
        self.lista_tablon = arcade.SpriteList()

        self.boton_atras = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "nivel" / "flecha_atras_menu.png"), scale = 1.8)
        self.tablon = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "controles"/ "tablon_controles.png"), scale = 0.5)

        self.lista_botones.append(self.boton_atras)
        self.lista_tablon.append(self.tablon)
        
    def on_show_view(self):

        centro_x = self.window.width / 2
        alto = self.window.height 
        
        self.boton_atras.center_x = 50
        self.boton_atras.center_y = alto - 50

        self.tablon.center_x = centro_x
        self.tablon.center_y = alto * (280/600)
    
    def on_draw(self):
        self.clear()
        
        centro_y = self.window.height / 2

        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, self.window.width, self.window.height))

        self.lista_botones.draw()
        self.lista_tablon.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Lógica para detectar clics y cambiar de vista
        """
        botones_pulsados = arcade.get_sprites_at_point((x, y), self.lista_botones)

        if len(botones_pulsados) > 0:
            boton_clicado = botones_pulsados[0]

            if boton_clicado == self.boton_atras:
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
    vista_controles = VistaControles()
    ventana.show_view(vista_controles)
    arcade.run()