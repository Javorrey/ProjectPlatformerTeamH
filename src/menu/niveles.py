import arcade

class VistaNiveles(arcade.View):
    def __init__(self):
        """
        Cargamos todas las imágenes.
        """
        super().__init__()

        self.fondo = arcade.load_texture("assets/images/menu/nivel/Fondo_menu.png")

        self.lista_botones = arcade.SpriteList()
        
        self.boton_nivel1 = arcade.Sprite("assets/images/menu/nivel/Botón_nivel1_menu.png", scale = 1.8)
        self.boton_nivel2 = arcade.Sprite("assets/images/menu/nivel/Botón_nivel2_menu.png", scale = 1.8)
        self.boton_nivel3 = arcade.Sprite("assets/images/menu/nivel/Botón_nivel3_menu.png", scale = 1.8)
        self.boton_nivel4 = arcade.Sprite("assets/images/menu/nivel/Botón_nivel4_menu.png", scale = 1.8)
        self.boton_nivel5 = arcade.Sprite("assets/images/menu/nivel/Botón_nivel5_menu.png", scale = 1.8)

        self.lista_botones.append(self.boton_nivel1)
        self.lista_botones.append(self.boton_nivel2)
        self.lista_botones.append(self.boton_nivel3)
        self.lista_botones.append(self.boton_nivel4)
        self.lista_botones.append(self.boton_nivel5)
        
    def on_show_view(self):
        centro_x = self.window.width / 2

        self.boton_nivel1.center_x = centro_x
        self.boton_nivel1.center_y = 370

        self.boton_nivel2.center_x = centro_x
        self.boton_nivel2.center_y = 300

        self.boton_nivel3.center_x = centro_x
        self.boton_nivel3.center_y = 230

        self.boton_nivel4.center_x = centro_x
        self.boton_nivel4.center_y = 160

        self.boton_nivel5.center_x = centro_x
        self.boton_nivel5.center_y = 90
    
    def on_draw(self):
        self.clear()
        
        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, self.window.width, self.window.height))

        self.lista_botones.draw()

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
    vista_nivel = VistaNiveles()
    ventana.show_view(vista_nivel)
    arcade.run()