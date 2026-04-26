import arcade

class VistaAjustes(arcade.View):
    def __init__(self):
        """
        Cargamos todas las imágenes.
        """
        super().__init__()

        arcade.load_font("assets/fonts/fuente_ajustes_menu.ttf")
        
        self.fondo = arcade.load_texture("assets/images/menu/ajustes/Fondo_menu.png")
        self.icono_sonido = arcade.load_texture("assets/images/menu/ajustes/icono_sonido_menu.png")
        self.icono_pantalla = arcade.load_texture("assets/images/menu/ajustes/icono_pantalla_menu.png")

        self.lista_botones = arcade.SpriteList()
        
        self.boton_atras = arcade.Sprite("assets/images/menu/ajustes/flecha_atras_menu.png", scale = 1.8)

        self.lista_botones.append(self.boton_atras)

    def on_show_view(self):
    
        self.boton_atras.center_x = 50
        self.boton_atras.center_y = 550

      
    def on_draw(self):
        self.clear()
        
        centro_x = self.window.width / 2
        
        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, self.window.width, self.window.height))
        
        arcade.draw_text("AJUSTES DE SONIDO", centro_x, 400, color=arcade.color.ORANGE_PEEL, font_size=27, font_name="Upheaval TT (BRK)", anchor_x="center")
        arcade.draw_texture_rect(self.icono_sonido, arcade.XYWH(200, 412, 50, 50))

        #arcade.draw_text("Música", 200, 350, color=arcade.color.WHITE, font_size=20, font_name="Upheaval TT (BRK)", anchor_x="center")

        arcade.draw_text("AJUSTES DE PANTALLA", centro_x + 17, 225, color=arcade.color.ORANGE_PEEL, font_size=27, font_name="Upheaval TT (BRK)", anchor_x="center")
        arcade.draw_texture_rect(self.icono_pantalla, arcade.XYWH(200, 237, 32, 32))

        self.lista_botones.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Lógica para detectar clics y cambiar de vista
        """
        botones_pulsados = arcade.get_sprites_at_point((x, y), self.lista_botones)

        if len(botones_pulsados) > 0:
            boton_clicado = botones_pulsados[0]

            if boton_clicado == self.boton_atras:
                from MainMenu import MainMenu
                proxima_vista = MainMenu()
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

if __name__ == '__main__':
    ventana = arcade.Window(800, 600, "Artemis 67")
    vista_ajustes = VistaAjustes()
    ventana.show_view(vista_ajustes)
    arcade.run()