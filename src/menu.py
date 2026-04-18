import arcade

class MainMenu(arcade.View):
    def __init__(self):
        """
        Cargamos todas las imágenes.
        """
        super().__init__()

        self.fondo = arcade.load_texture("assets/images/menu/Fondo_menu.png")

        self.lista_botones = arcade.SpriteList()
        
        self.boton_jugar = arcade.Sprite("assets/images/menu/Botón_jugar_menu.png", scale = 1.8)
        self.boton_nivel = arcade.Sprite("assets/images/menu/Botón_nivel_menu.png", scale = 1.8)
        self.boton_ajustes = arcade.Sprite("assets/images/menu/Botón_ajustes_menu.png", scale = 1.8)
        self.boton_salir = arcade.Sprite("assets/images/menu/Botón_salir_menu.png", scale = 1.8)

        self.lista_botones.append(self.boton_jugar)
        self.lista_botones.append(self.boton_nivel)
        self.lista_botones.append(self.boton_ajustes)
        self.lista_botones.append(self.boton_salir)

    def on_show_view(self):
        centro_x = self.window.width / 2

        self.boton_jugar.center_x = centro_x
        self.boton_jugar.center_y = 240

        self.boton_nivel.center_x = centro_x
        self.boton_nivel.center_y = 180

        self.boton_ajustes.center_x = centro_x
        self.boton_ajustes.center_y = 120

        self.boton_salir.center_x = centro_x
        self.boton_salir.center_y = 60

    def on_draw(self):
        self.clear()
        
        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, self.window.width, self.window.height))

        self.lista_botones.draw()

if __name__ == '__main__':
    ventana = arcade.Window(800, 600, "Artemises 67 - Menú Principal")
    vista_menu = MainMenu()
    ventana.show_view(vista_menu)
    arcade.run()
