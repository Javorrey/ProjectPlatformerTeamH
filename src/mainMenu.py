import arcade

from niveles import VistaNiveles
from ajustes import VistaAjustes
from controles import VistaControles

import sys
from pathlib import Path

import serializacion
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
        self.lista_mando = arcade.SpriteList()
        
        self.boton_jugar = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "main" / "boton_jugar_menu.png"), scale = 1.8)
        self.boton_reinicio = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "main" / "boton_nivel_menu.png"), scale = 1.8)
        self.boton_ajustes = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "main" / "boton_ajustes_menu.png"), scale = 1.8)
        self.boton_salir = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "main" / "boton_salir_menu.png"), scale = 1.8)
        self.boton_controles = arcade.Sprite(str(BASE_DIR / "assets" / "images" / "menu" / "main" / "mando_controles_menu.png"), scale = 0.075)

        self.lista_botones.append(self.boton_jugar)
        self.lista_botones.append(self.boton_reinicio)
        self.lista_botones.append(self.boton_ajustes)
        self.lista_botones.append(self.boton_salir)
        self.lista_mando.append(self.boton_controles)

    def on_show_view(self):
        #Si no hay música sonando, la cargamos y la encendemos por primera vez
        if not hasattr(self.window, "reproductor_menu") or self.window.reproductor_menu is None:
            
            ruta_musica_menu = str(BASE_DIR / "assets" / "music" / "Mythical Axiom.mp3")
            self.window.musica_menu = arcade.load_sound(ruta_musica_menu)
            
            volumen_actual = getattr(self.window, "volumen_musica", 0.7)
            
            self.window.reproductor_menu = self.window.musica_menu.play(
                volume=volumen_actual, 
                loop=True
            )
            
        #Si ya existía, nos aseguramos de que siga sonando
        else:
            self.window.reproductor_menu.play()

        centro_x = self.window.width / 2
        alto = self.window.height
        ancho = self.window.width

        self.boton_jugar.center_x = centro_x
        self.boton_jugar.center_y = alto * (340/600)

        self.boton_reinicio.center_x = centro_x
        self.boton_reinicio.center_y = alto * (270/600)

        self.boton_ajustes.center_x = centro_x
        self.boton_ajustes.center_y = alto * (200/600)

        self.boton_salir.center_x = centro_x
        self.boton_salir.center_y = alto * (130/600)

        self.boton_controles.center_x = ancho - 50
        self.boton_controles.center_y = alto - 50

    def setup(self):
        self.reproductor_musica = arcade.play_sound(self.musica_fondo, volume=0.2, loop=True)

    def on_draw(self):
        self.clear()
        
        centro_x = self.window.width / 2

        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, self.window.width, self.window.height))

        self.lista_botones.draw()
        self.lista_mando.draw()

        texto_nivel = f"Nivel seleccionado: {self.window.nivel_seleccionado}"
        texto_nivel_x = 150
        texto_nivel_y = 50
        arcade.draw_text(texto_nivel, texto_nivel_x, texto_nivel_y, color=arcade.color.WHITE, font_size=15, font_name="Upheaval TT (BRK)", anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Lógica para detectar clics y cambiar de vista
        """
        botones_pulsados = arcade.get_sprites_at_point((x, y), self.lista_botones)
        mando_pulsado = arcade.get_sprites_at_point((x, y), self.lista_mando)

        if len(botones_pulsados) > 0:
            boton_clicado = botones_pulsados[0]

            if boton_clicado == self.boton_jugar:
                if hasattr(self.window, "reproductor_menu") and self.window.reproductor_menu is not None:
                    # Detenemos el sonido de la ventana
                    arcade.stop_sound(self.window.reproductor_menu)
                    self.window.reproductor_menu = None
                    
                vista_juego = self.window.GameViewClass()
                self.window.show_view(vista_juego)

            if boton_clicado == self.boton_reinicio:
                serializacion.guardar_datos(DATOS_INICIALES)

                # Actualizar datos en memoria
                self.window.datos_guardados = DATOS_INICIALES.copy()
                self.window.nivel_seleccionado = DATOS_INICIALES["nivel_desbloqueado"]

            elif boton_clicado == self.boton_ajustes:
                proxima_vista = VistaAjustes()
                self.window.show_view(proxima_vista)

            elif boton_clicado == self.boton_salir:
                arcade.exit()

        if len(mando_pulsado) > 0:
            boton_clicado = mando_pulsado[0]

            if boton_clicado == self.boton_controles:
                proxima_vista = VistaControles()
                self.window.show_view(proxima_vista)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Función para añadir efectos cuando se pasa la flecha del ratón por encima de los botones
        """
        #Reseteo
        for boton in self.lista_botones:
            boton.scale = 1.8

        for boton in self.lista_mando:
            boton.scale = 0.075
        
        #Detección
        botones_tocados = arcade.get_sprites_at_point((x, y), self.lista_botones)
        mando_tocado = arcade.get_sprites_at_point((x, y), self.lista_mando)

        #Efecto
        if len(botones_tocados) > 0:
            boton_actual = botones_tocados[0]
            boton_actual.scale = 2.0

        if len(mando_tocado) > 0:
            boton_actual = mando_tocado[0]
            boton.scale = 0.095

if __name__ == '__main__':
    ventana = arcade.Window(800, 600, "Artemis 67")
    
    #Registramos la ventana
    ventana.MainMenuClass = mainMenu

    ventana.nivel_seleccionado = 1
    
    #ventana.volumen_seleccionado = 0.7  terminar cuando elijamos musica

    vista_menu = mainMenu()
    vista_menu.setup()
    ventana.show_view(vista_menu)
    arcade.run()
