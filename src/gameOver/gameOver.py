import arcade

class GameOver(arcade.View):
    def __init__(self):
        """
        Inicializamos la vista y cargamos todos los recursos
        """
        super().__init__()
        
        self.fondo = arcade.load_texture("assets/images/gameOver/fondo_game_over.png")

        self.lista_botones = arcade.SpriteList()
        
        self.boton_volver_a_jugar = arcade.Sprite("assets/images/gameOver/boton_volver_a_jugar_game_over.png", scale = 1.8)
        self.boton_ir_al_menu = arcade.Sprite("assets/images/gameOver/boton_ir_al_menu_game_over.png", scale=1.8)

        self.lista_botones.append(self.boton_volver_a_jugar)
        self.lista_botones.append(self.boton_ir_al_menu)

    def on_show_view(self):
        centro_x = self.window.width / 2
        alto = self.window.height

        self.boton_volver_a_jugar.center_x = centro_x
        self.boton_volver_a_jugar.center_y = alto * (290/600)

        self.boton_ir_al_menu.center_x = centro_x
        self.boton_ir_al_menu.center_y = alto * (200/600)

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

            #if boton_clicado == self.boton_volver_a_jugar:
        
            if boton_clicado == self.boton_ir_al_menu:
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

if __name__ == '__main__':
    ventana = arcade.Window(800, 600, "Artemis 67")
    vista_game_over = GameOver()
    ventana.show_view(vista_game_over)
    arcade.run()
