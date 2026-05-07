import arcade

class VistaAjustes(arcade.View):
    def __init__(self):
        """
        Inicializamos la vista y cargamos todos los recursos
        """
        super().__init__()

        arcade.load_font("assets/fonts/fuente_menu.ttf")
        
        self.fondo = arcade.load_texture("assets/images/menu/ajustes/fondo_menu.png")
        self.icono_sonido = arcade.load_texture("assets/images/menu/ajustes/icono_sonido_menu.png")
        self.icono_pantalla = arcade.load_texture("assets/images/menu/ajustes/icono_pantalla_menu.png")

        self.lista_botones = arcade.SpriteList()
        
        self.boton_atras = arcade.Sprite("assets/images/menu/ajustes/flecha_atras_menu.png", scale = 1.8)

        self.lista_botones.append(self.boton_atras)

        #Variables para la línea del volumen
        self.volumen_musica = 0.7  #Volumen por defecto = 70%
        self.slider_ancho = 200    #La línea mide 200 pixeles de largo
        self.slider_alto = 20      #Área invisible para que sea fácil hacer click
        
        self.slider_x = 0
        self.slider_y = 0
        self.arrastrando_slider = False

        #Variables para el interruptor (Toggle) de pantalla completa
        self.toggle_ancho = 60
        self.toggle_alto = 30
        self.toggle_x = 0
        self.toggle_y = 0

    def on_show_view(self):
        alto = self.window.height

        self.boton_atras.center_x = 50
        self.boton_atras.center_y = alto - 50
      
    def on_draw(self):
        self.clear()
        
        centro_x = self.window.width / 2
        alto = self.window.height
        
        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, self.window.width, self.window.height))
        
        #AJUSTES DE SONIDO
        #Posiciones
        texto_ajustes_de_sonido_x = centro_x
        texto_ajustes_de_sonido_y = alto * (400/600)

        icono_sonido_x = centro_x - 200
        icono_sonido_y = texto_ajustes_de_sonido_y + 10

        texto_musica_x = centro_x - 130
        texto_musica_y = alto * (350/600)

        self.slider_x = centro_x - 30
        self.slider_y = texto_musica_y + 7
        
        ancho_relleno_slider = self.slider_ancho * self.volumen_musica

        #Dibujo
        arcade.draw_text("AJUSTES DE SONIDO:", texto_ajustes_de_sonido_x, texto_ajustes_de_sonido_y, color=arcade.color.ORANGE_PEEL, font_size=27, font_name="Upheaval TT (BRK)", anchor_x="center")
        arcade.draw_texture_rect(self.icono_sonido, arcade.XYWH(icono_sonido_x, icono_sonido_y, 50, 50))

        arcade.draw_text("Música:", texto_musica_x, texto_musica_y, color=arcade.color.WHITE, font_size=20, font_name="Upheaval TT (BRK)", anchor_x="center")
        
        arcade.draw_line(self.slider_x, self.slider_y, self.slider_x + self.slider_ancho, self.slider_y, arcade.color.DARK_GRAY, line_width=6)
        arcade.draw_line(self.slider_x, self.slider_y, self.slider_x + ancho_relleno_slider, self.slider_y, arcade.color.CYAN, line_width=6)
        arcade.draw_circle_filled(self.slider_x + ancho_relleno_slider, self.slider_y, 10, arcade.color.WHITE)

        #AJUSTES DE PANTALLA
        #Posiciones
        texto_ajustes_de_pantalla_x = centro_x + 22
        texto_ajustes_de_pantalla_y = alto * (225/600)

        icono_pantalla_x = centro_x - 200
        icono_pantalla_y = texto_ajustes_de_pantalla_y + 12

        texto_pantalla_completa_x = centro_x - 180
        texto_pantalla_completa_y = alto * (175/600)

        self.toggle_x = centro_x + 130
        self.toggle_y = texto_pantalla_completa_y

        #Elegimos el color del fondo del toggle según si está activado o no
        if self.window.fullscreen:
            color_fondo = arcade.color.APPLE_GREEN 
        else:
            color_fondo = arcade.color.DARK_GRAY   
        
        #Dibujo
        arcade.draw_text("AJUSTES DE PANTALLA:", texto_ajustes_de_pantalla_x, texto_ajustes_de_pantalla_y, color=arcade.color.ORANGE_PEEL, font_size=27, font_name="Upheaval TT (BRK)", anchor_x="center")
        arcade.draw_texture_rect(self.icono_pantalla, arcade.XYWH(icono_pantalla_x, icono_pantalla_y, 32, 32))
        
        arcade.draw_text("Pantalla completa:", texto_pantalla_completa_x, texto_pantalla_completa_y, color=arcade.color.WHITE, font_size=20, font_name="Upheaval TT (BRK)", anchor_x="left", anchor_y="center")

        arcade.draw_rect_filled(arcade.XYWH(self.toggle_x, self.toggle_y, self.toggle_ancho, self.toggle_alto), color_fondo)

        #Calculamos dónde va el circulito blanco (el tirador)
        if self.window.fullscreen:
            circulo_x = self.toggle_x + 15 
        else:
            circulo_x = self.toggle_x - 15 

        arcade.draw_circle_filled(circulo_x, self.toggle_y, 12, arcade.color.WHITE)

        self.lista_botones.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Lógica para detectar clics y cambiar de vista
        """
        botones_pulsados = arcade.get_sprites_at_point((x, y), self.lista_botones)

        if len(botones_pulsados) > 0:
            boton_clicado = botones_pulsados[0]

            if boton_clicado == self.boton_atras:
                from mainMenu import mainMenu
                proxima_vista = mainMenu()
                self.window.show_view(proxima_vista)

        #LÓGICA DEL SLIDER
        #Si la flecha del ratón esta entre el comienzo y el final del slider y si esta 20 pixeles por debajo o por encima del slider
        if (self.slider_x <= x <= self.slider_x + self.slider_ancho and self.slider_y - self.slider_alto <= y <= self.slider_y + self.slider_alto):
            self.arrastrando_slider = True
            self.actualizar_volumen_desde_raton(x)

        #LÓGICA DEL TOGGLE
        mitad_ancho_toggle = self.toggle_ancho / 2
        mitad_alto_toggle = self.toggle_alto / 2
        
        if (self.toggle_x - mitad_ancho_toggle <= x <= self.toggle_x + mitad_ancho_toggle and self.toggle_y - mitad_alto_toggle <= y <= self.toggle_y + mitad_alto_toggle):
            # Cambia la pantalla completa
            self.window.set_fullscreen(not self.window.fullscreen)

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Lógica para detectar cuando se suelta el clic del ratón
        """
        self.arrastrando_slider = False

    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        """
        Lógica para detectar si movemos el ratón mientras le tenemos pulsado
        """
        if self.arrastrando_slider:
            self.actualizar_volumen_desde_raton(x)

    def actualizar_volumen_desde_raton(self, raton_x):
        """
        Calcula el nivel de volumen exacto segun la posición del ratón
        """
        posicion_relativa = raton_x - self.slider_x
        nuevo_volumen = posicion_relativa / self.slider_ancho
        self.volumen_musica = max(0.0, min(1.0, nuevo_volumen))

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
    vista_ajustes = VistaAjustes()
    ventana.show_view(vista_ajustes)
    arcade.run()