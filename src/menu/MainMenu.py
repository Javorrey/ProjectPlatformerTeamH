import arcade

from niveles import VistaNiveles

class MainMenu(arcade.View):
    def __init__(self):
        """
        Cargamos todas las imágenes.
        """
        super().__init__()

        self.fondo = arcade.load_texture("assets/images/menu/main/Fondo_menu.png")

        self.lista_botones = arcade.SpriteList()
        
        self.boton_jugar = arcade.Sprite("assets/images/menu/main/Botón_jugar_menu.png", scale = 1.8)
        self.boton_nivel = arcade.Sprite("assets/images/menu/main/Botón_nivel_menu.png", scale = 1.8)
        self.boton_ajustes = arcade.Sprite("assets/images/menu/main/Botón_ajustes_menu.png", scale = 1.8)
        self.boton_salir = arcade.Sprite("assets/images/menu/main/Botón_salir_menu.png", scale = 1.8)

        self.lista_botones.append(self.boton_jugar)
        self.lista_botones.append(self.boton_nivel)
        self.lista_botones.append(self.boton_ajustes)
        self.lista_botones.append(self.boton_salir)

    def on_show_view(self):
        centro_x = self.window.width / 2

        self.boton_jugar.center_x = centro_x
        self.boton_jugar.center_y = 340

        self.boton_nivel.center_x = centro_x
        self.boton_nivel.center_y = 270

        self.boton_ajustes.center_x = centro_x
        self.boton_ajustes.center_y = 200

        self.boton_salir.center_x = centro_x
        self.boton_salir.center_y = 130

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

            #if boton_clicado == self.boton_jugar:
                #Nueva vista
            if boton_clicado == self.boton_nivel:
                proxima_vista = VistaNiveles()
                self.window.show_view(proxima_vista)
            #elif boton_clicado == self.boton_ajustes:
                #Nueva vista
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
    vista_menu = MainMenu()
    ventana.show_view(vista_menu)
    arcade.run()
