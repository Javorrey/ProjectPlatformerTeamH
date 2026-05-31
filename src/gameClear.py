import arcade
import constants as cts
from mainMenu import mainMenu

class GameClearView(arcade.View):
    def __init__(self, final_score, piezas_recogidas_dict):
        super().__init__()
        self.final_score = final_score
        
        # Contamos cuántas piezas se recogieron en total a lo largo de los niveles
        # Convierte los valores a int por si se guardaron como strings o booleanos
        self.total_piezas = sum(int(valor) for valor in piezas_recogidas_dict.values())
        
        # Si tienes un total máximo de niveles (ej. 5), lo ponemos aquí
        self.max_piezas = len(piezas_recogidas_dict) 

    def on_show_view(self):
        # Aseguramos que el ratón vuelva a ser visible
        self.window.set_mouse_visible(True)

    def on_draw(self):
        self.clear()

        # Fondo oscuro/azul espacial para celebrar la victoria
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        
        ancho = self.window.width
        alto = self.window.height

        # --- TÍTULO PRINCIPAL ---
        arcade.draw_text(
            "¡FELICIDADES!",
            ancho // 2,
            alto // 2 + 150,
            arcade.color.GOLD,
            font_size=50,
            font_name="Upheaval TT (BRK)",
            anchor_x="center"
        )
        arcade.draw_text(
            "HAS COMPLETADO EL JUEGO",
            ancho // 2,
            alto // 2 + 100,
            arcade.color.WHITE,
            font_size=25,
            font_name="Upheaval TT (BRK)",
            anchor_x="center"
        )

        # --- ESTADÍSTICAS ---
        # Recuadro de fondo para las estadísticas
        arcade.draw_lrbt_rectangle_filled(
            left=ancho // 2 - 200,
            right=ancho // 2 + 200,
            top=alto // 2 + 40,
            bottom=alto // 2 - 100,
            color=(0, 0, 0, 100)
        )

        # Puntuación Final
        arcade.draw_text(
            f"PUNTUACIÓN TOTAL: {self.final_score}",
            ancho // 2,
            alto // 2,
            arcade.color.LIGHT_GREEN,
            font_size=22,
            font_name="Upheaval TT (BRK)",
            anchor_x="center"
        )

        # Piezas Conseguidas
        arcade.draw_text(
            f"PIEZAS ENCONTRADAS: {self.total_piezas} / {self.max_piezas}",
            ancho // 2,
            alto // 2 - 50,
            arcade.color.AQUAMARINE,
            font_size=22,
            font_name="Upheaval TT (BRK)",
            anchor_x="center"
        )

        # --- INSTRUCCIONES DE NAVEGACIÓN ---
        arcade.draw_text(
            "Presiona ENTER para volver al Menú Principal",
            ancho // 2,
            alto // 2 - 180,
            arcade.color.LIGHT_GRAY,
            font_size=16,
            font_name="Upheaval TT (BRK)",
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        # Al presionar ENTER volvemos al menú
        if key == arcade.key.ENTER:
            cts.PLAYING_LEVEL = False
            menu_view = mainMenu()
            self.window.show_view(menu_view)