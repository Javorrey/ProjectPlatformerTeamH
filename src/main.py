"""
Platformer Game. 

Basado en el tutorial de arcade: https://arcade.academy/examples/platform_tutorial.html#platform-tutorial
"""
from itertools import count
import math

from pathlib import Path

import arcade

from character import *
from constants import *
import constants as cts
from projectile import *

from mainMenu import mainMenu
from niveles import VistaNiveles
from ajustes import VistaAjustes

from gameOver import GameOver

def preload_assets(route, columnas, cantidad):
    path_or_texture = str(PROJECTILE_PATH / route)
    texture_sheet = arcade.load_spritesheet(path_or_texture)
    texture_list = texture_sheet.get_texture_grid(
        size=(64, 64),  
        columns=columnas,      
        count=cantidad         
    )
    return texture_list

class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # Track the current state of our input
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.shoot_pressed = False
        self.shoot_explosivo_pressed = False

        self.velocidad_bala_x= 12 #12
        self.velocidad_bala_y= 0

        # Variable to hold our texture for our player
        self.player_texture = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Variable to hold our Tiled Map
        self.tile_map = None

        # Replacing all of our SpriteLists with a Scene variable
        self.scene = None

        # A variable to store our camera object
        self.camera = None

        # A variable to store our gui camera object
        self.gui_camera = None

        # This variable will store our score as an integer.
        self.score = 0

        # This variable will store the text for score that we will draw to the screen.
        self.score_text = None

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Should we reset the score?
        self.reset_score = True

        # Shooting mechanics
        self.can_shoot = False
        self.shoot_timer = 0

        self.can_shoot_explosivo = True
        self.timer_explosivo = 0.0
        self.COOLDOWN_EXPLOSIVO = 3.0

        #Load font
        arcade.load_font(str(BASE_DIR / "assets" / "fonts" / "fuente_menu.ttf"))

        #Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.gameover_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.shoot_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

        self.physics_engine = None 

        #Load Sprites
        self.primaryFire_texture_list = preload_assets("Friendly Fire 2.0.png", 2, 5)
        self.secondaryFire_texture_list = preload_assets("Friendly Bomb 2.0.png", 2, 5)
        self.enemy_bullet_texture_list = preload_assets("enemy_fire_3.0.png", 2, 5)
        self.secondaryFireCharge_texture_list = preload_assets("Charging (1).png", 3, 10)
        

        self.gui_sprites = arcade.SpriteList()
        self.secondaryFireChargeSprite = arcade.Sprite(self.secondaryFireCharge_texture_list[8])
        self.secondaryFireChargeSprite.right = WINDOW_WIDTH - 30
        self.secondaryFireChargeSprite.bottom = 30
        self.gui_sprites.append(self.secondaryFireChargeSprite)

        ruta_musica = str(BASE_DIR / "assets" / "music" / "Phase Shift.mp3")
        self.musica_fondo = arcade.load_sound(ruta_musica)
        self.reproductor_musica = None

    def setup(self):
        cts.PLAYING_LEVEL = True
        """Set up the game here. Call this function to restart the game."""
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True
            },
            "Moving_Platforms": {
                "use_spatial_hash": False
            },
            "Ladders": {
                "use_spatial_hash": True
            }
        }

        #CARGA DEL NIVEL SELECCIONADO
        ruta_mapa = obtener_ruta_mapa(self.window.nivel_seleccionado)
        #escala todo en base al tamaño de la pantalla
        factor_escala=self.window.width/1280
        cts.TILE_SCALING = TILE_SCALING * factor_escala
        cts.CHARACTER_SCALING = CHARACTER_SCALING* factor_escala
        
        cts.PLAYER_MOVEMENT_SPEED = 5 * cts.TILE_SCALING
        cts.GRAVITY = GRAVITY*cts.TILE_SCALING
        cts.PLAYER_JUMP_SPEED =PLAYER_JUMP_SPEED * cts.TILE_SCALING

        self.tile_map = arcade.load_tilemap(
            ruta_mapa,
            scaling=cts.TILE_SCALING,
            layer_options=layer_options,
        )

        # Create our Scene Based on the TileMap
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        #ajusta los moving_platforms con el tamaño de la pantalla
        for platform in self.scene["Moving_Platforms"]:

            if hasattr(platform, "boundary_left") and platform.boundary_left is not None:
                platform.boundary_left *= cts.TILE_SCALING

            if hasattr(platform, "boundary_right") and platform.boundary_right is not None:
                platform.boundary_right *= cts.TILE_SCALING

            if hasattr(platform, "boundary_top") and platform.boundary_top is not None:
                platform.boundary_top *= cts.TILE_SCALING

            if hasattr(platform, "boundary_bottom") and platform.boundary_bottom is not None:
                platform.boundary_bottom *= cts.TILE_SCALING
        #Daño que soporta una pared de este layer
        for bloque in self.scene["Paredes_Destructibles"]:
            bloque.health= 50

        self.player_sprite = PlayerCharacter()
        self.player_sprite.scale= cts.CHARACTER_SCALING #personaje escalado con la pantalla
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # -- Enemies
        enemies_layer = self.tile_map.object_lists["Enemies"]
        ENEMY_TYPES = {
                "alien": AlienEnemy, 
                "zombie": ZombieEnemy,
            }
     
            
        # Create a Platformer Physics Engine, this will handle moving our
        # player as well as collisions between the player sprite and
        # whatever SpriteList we specify for the walls.
        # It is important to supply static to the walls parameter. There is a
        # platforms parameter that is intended for moving platforms.
        # If a platform is supposed to move, and is added to the walls list,
        # it will not be moved.
        
        self.mis_paredes= [self.scene["walls"], self.scene["Platforms"], self.scene["Paredes_Destructibles"]]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.mis_paredes,
            gravity_constant=cts.GRAVITY,
            platforms=self.scene["Moving_Platforms"],
            
        )
        self.enemy_engines = []
        for enemy_marker in enemies_layer:
            coordinates = self.tile_map.get_cartesian(
                enemy_marker.shape[0], enemy_marker.shape[1]
            )
            
            enemy_type = enemy_marker.properties["type"]
            enemy_class = ENEMY_TYPES.get(enemy_type)

            if enemy_class is None:
                continue

            enemy = enemy_class()
            #Pasar el juego al enemigo para que pueda "ver" al jugador
            enemy.juego = self
            

            enemy.center_x = math.floor(
                (coordinates[0]+1) * cts.TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (coordinates[1] +1) * (self.tile_map.tile_height * cts.TILE_SCALING)
            )
            if "boundary_left" in enemy_marker.properties:
                enemy.boundary_left = enemy_marker.properties["boundary_left"]*cts.TILE_SCALING
            if "boundary_right" in enemy_marker.properties:
                enemy.boundary_right = enemy_marker.properties["boundary_right"]*cts.TILE_SCALING
            if "change_x" in enemy_marker.properties:
                enemy.change_x = enemy_marker.properties["change_x"]
            enemy.scale=cts.CHARACTER_SCALING

            self.scene.add_sprite("Enemies", enemy)
            engine = arcade.PhysicsEnginePlatformer(enemy, walls=self.mis_paredes, gravity_constant=GRAVITY,)
            self.enemy_engines.append(engine)

        self.enemigos_cercanos = set()

        # Initialize our camera, setting a viewport the size of our window.
        self.camera = arcade.Camera2D()

        # Initialize our gui camera, initial settings are the same as our world camera.
        self.gui_camera = arcade.Camera2D()
        self.score=0
        # Reset the score if we should
        if self.reset_score:
            self.score = 0
        self.reset_score = True

        # Shooting mechanics
        self.can_shoot = False
        self.shoot_timer = 0

        # Initialize our arcade.Text object for score
        self.score_text = arcade.Text(f"Score: {self.score}", x=0, y=5)

        #self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Calculate the right edge of the map in pixels
        self.end_of_map = (self.tile_map.width * self.tile_map.tile_width)
        self.end_of_map *= self.tile_map.scaling
        # calcula el top del mapa
        self.top_of_map=(self.tile_map.height*self.tile_map.tile_height)* self.tile_map.scaling

        # Add an empty bullet SpriteList to our scene
        self.scene.add_sprite_list("Bullets")
        self.scene.add_sprite_list("Balas_Enemigas")
        # Comprobar si el jugador cogió la pieza
        self.pieza_recogida= False


        if self.tile_map.background_color:
            self.window.background_color = self.tile_map.background_color
        else:
            self.window.background_color = arcade.color.CORNFLOWER_BLUE
        if self.reproductor_musica is not None:
            self.reproductor_musica.pause()


        self.reproductor_musica = arcade.play_sound(self.musica_fondo, volume=0.3, loop=True)


    def on_show_view(self):
        if cts.PLAYING_LEVEL == False:
            self.setup()
        else:
            if self.reproductor_musica is not None:
                self.reproductor_musica.play()

    def on_draw(self):
        """Render the screen."""

        if not self.camera:
            return

        # Clear the screen to the background color
        self.clear()
     
        # Activate our camera before drawing
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate our GUI camera
        self.gui_camera.use()

        # Draw our Score
        self.score_text.draw()

        #Draw secondary fire charge status
        if self.can_shoot_explosivo:
            self.secondaryFireChargeSprite.texture = self.secondaryFireCharge_texture_list[8]
        else:
            self.secondaryFireChargeSprite.texture = self.secondaryFireCharge_texture_list[0]
        self.gui_sprites.draw()

    def on_update(self, delta_time):
        """Movement and Game Logic"""
        
        if not self.physics_engine:
            return
        
        # Move the player using our physics engine
        self.physics_engine.update()

        #Búsqueda espacial para todos los enemigos
        self.enemigos_cercanos = set()
        RADIO_ACTIVACION = 2000 
        for enemy in self.scene["Enemies"]:
            dx = enemy.center_x - self.player_sprite.center_x
            dy = enemy.center_y - self.player_sprite.center_y
            if (dx*dx + dy*dy) <= (RADIO_ACTIVACION ** 2):
                self.enemigos_cercanos.add(enemy)

        #Físicas de los enemigos cercanos
        for engine in self.enemy_engines:
            if engine.player_sprite in self.enemigos_cercanos:
                engine.update()

        # Update our characters animation state
        if self.physics_engine.is_on_ladder():
            self.player_sprite.climbing = True
        else:
            self.player_sprite.climbing = False

        self.player_sprite.is_on_ground = self.physics_engine.can_jump()

        self.player_sprite.change_y_aim = self.velocidad_bala_y
        self.player_sprite.change_x_aim = self.velocidad_bala_x 

        # ---------------- LOGICA DE DISPARO NORMAL ----------------
        if self.can_shoot:
            if self.shoot_pressed:
                arcade.play_sound(self.shoot_sound)
                
                # Calcular velocidad X según a dónde mira
                vel_x = self.velocidad_bala_x if self.player_sprite.facing_direction == RIGHT_FACING else -self.velocidad_bala_x
                vel_y = self.velocidad_bala_y
                
                # Usar la nueva clase LaserAzul
                bullet = DisparoPrincipal(
                    self.player_sprite.center_x - 12, 
                    self.player_sprite.center_y - 4, 
                    vel_x, 
                    vel_y,
                    self,
                    self.primaryFire_texture_list
                )

                self.scene.add_sprite("Bullets", bullet)
                self.can_shoot = False
        else:
            self.shoot_timer += 1
            if self.shoot_timer == 15:
                self.can_shoot = True
                self.shoot_timer = 0

        # ---------------- LOGICA DE DISPARO EXPLOSIVO ----------------
        if self.can_shoot_explosivo:
            if self.shoot_explosivo_pressed:
                arcade.play_sound(self.shoot_sound)
                
                vel_x = self.velocidad_bala_x if self.player_sprite.facing_direction == RIGHT_FACING else -self.velocidad_bala_x
                vel_y = self.velocidad_bala_y
                
                # Usar la clase ProyectilExplosivo
                misil = DisparoSecundario(
                    self.player_sprite.center_x - 12, 
                    self.player_sprite.center_y - 4, 
                    vel_x, 
                    vel_y,
                    self,
                    self.secondaryFire_texture_list
                )
                
                self.scene.add_sprite("Bullets", misil)
                
                # Desactivar el arma hasta que pase el cooldown
                self.can_shoot_explosivo = False
                # Fuerza a soltar el clic para que no dispare en ráfaga automática
                self.shoot_explosivo_pressed = False 
        else:
            # Si no puede disparar, el temporizador empieza a contar
            self.timer_explosivo += delta_time
            if self.timer_explosivo >= self.COOLDOWN_EXPLOSIVO:
                self.can_shoot_explosivo = True
                self.timer_explosivo = 0.0


        # Actually trigger animation updates. We've added the Background and Coins layer
        # here as well. Our Tiled map has some animated tiles built-in, check out the flags
        # and torches on the map.
        self.scene.update_animation(
            delta_time,
            [
               
                "Background",
                "Player",
                "Enemies"
            ]
        )

        self.scene.update(delta_time, ["Enemies", "Bullets", "Balas_Enemigas"])

        # Límites de patrulla
        for enemy in self.scene["Enemies"]:
            if hasattr(enemy, "boundary_right") and hasattr(enemy, "boundary_left"):
                distancia = arcade.get_distance_between_sprites(enemy, self.player_sprite)
                if distancia >= ZOMBIE_VISION_RANGE:  # solo en modo patrulla
                    if enemy.right > enemy.boundary_right and enemy.change_x > 0:
                        enemy.change_x *= -1
                    elif enemy.left < enemy.boundary_left and enemy.change_x < 0:
                        enemy.change_x *= -1
        
        # ---------------- COLISIONES MORTALES ----------------

        # Colisión con enemigos
        enemigos_collision = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.scene["Enemies"]
        )

        # Colisión con zonas de daño
        danio_collision = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.scene["Daño"]
        )

        # Colisión con balas enemigas
        balas_collision = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.scene["Balas_Enemigas"]
        )

        # Si toca cualquiera de las tres cosas -> muere
        if enemigos_collision or danio_collision or balas_collision:

            # Eliminar balas enemigas que impactaron
            for bala in balas_collision:
                bala.remove_from_sprite_lists()

            if self.reproductor_musica:
                self.reproductor_musica.pause()

            cts.PLAYING_LEVEL = False

            arcade.play_sound(self.gameover_sound)

            game_over = GameOver()
            self.window.show_view(game_over)

            return  
        colisiones_obj= arcade.check_for_collision_with_list(
            self.player_sprite,
            self.scene["Items"]
        )

        for objeto in colisiones_obj:
            if objeto.properties["type"] == "pieza":
                objeto.remove_from_sprite_lists()
                objeto.kill()
                arcade.play_sound(self.collect_coin_sound)
                self.pieza_recogida= True
                self.score +=75
                self.score_text.text= f"Score: {self.score}"               
              
            elif objeto.properties["type"] == "portal":
                if self.pieza_recogida:
                    self.reproductor_musica.pause()
                    cts.PLAYING_LEVEL = False
                    game_over = GameOver()
                    self.window.show_view(game_over)
                    return
                else:
                    pass
                    
        #metodo que centra la camara en base a la posicion del player
        self.center_camera_to_player()

    def center_camera_to_player(self):
        ancho_ventana = self.window.width
        alto_ventana = self.window.height
        # Limite izquierdo
        if self.player_sprite.center_x <= ancho_ventana // 2:
            camera_x = ancho_ventana // 2
        # Limite derecho
        elif self.player_sprite.center_x >= (self.end_of_map - ancho_ventana // 2):
            camera_x = self.end_of_map - ancho_ventana // 2
        # Seguir jugador
        else:
            camera_x = self.player_sprite.center_x
        # Centrar cámara
        self.camera.position = (
            camera_x,
            alto_ventana // 2
        )  

    def process_keychange(self):
        # First handle the case where we have moved up. This needs to be handled
        # differently to move the player upwards if they are on a ladder, or
        # perform a jump if they are not on a ladder. This code might look
        # different if we had a separate button for jumping, we would only need
        # to handle moving upwards if we were on a ladder for the up key then.
        # Here we also handle the case where we have moved down while on a ladder.
        if self.physics_engine is None:
            return
        
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = cts.PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump(y_distance=10):
                self.player_sprite.change_y = cts.PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -cts.PLAYER_MOVEMENT_SPEED

        # Now we need a special handling of our vertical movement while we are 
        # on a ladder, but have no input specified. When we jump, the physics
        # engine takes care of resetting our vertical movement to zero once we've
        # hit the ground. However for ladders, we need to ensure that we set the
        # vertical movement back to zero if the user does not give input, otherwise
        # once a user starts climbing a ladder, they will move upwards automatically
        # until they reach the end of the ladder. You can try commenting out this
        # block to see what that effect looks like.
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Now we just handle our horizontal movement, very similar to how we
        # did before, but now just combined in our new function.
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = cts.PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -cts.PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shoot_pressed = True
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.shoot_explosivo_pressed = True
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shoot_pressed = False
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.shoot_explosivo_pressed = False
    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.ESCAPE:
            self.reproductor_musica.pause()
            pause_view = PauseView(self)
            self.window.show_view(pause_view)

        if key == arcade.key.UP or key == arcade.key.W:
            if self.velocidad_bala_x == 0 and self.velocidad_bala_y == 12:
                return
            elif self.velocidad_bala_y >= 0:
                self.velocidad_bala_y += 6
                self.velocidad_bala_x -=6
            else:
                self.velocidad_bala_y += 6
                self.velocidad_bala_x +=6
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.velocidad_bala_x ==0 and self.velocidad_bala_y == -12:
                return
            elif self.velocidad_bala_y <= 0:
                self.velocidad_bala_y -= 6
                self.velocidad_bala_x -=6
            else:
                self.velocidad_bala_y -= 6
                self.velocidad_bala_x +=6
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key ==arcade.key.SPACE:
            self.up_pressed = True
        elif key == arcade.key.J:
            self.shoot_pressed = True
        elif key == arcade.key.K:
            self.shoot_explosivo_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key ==arcade.key.SPACE:
            self.up_pressed = False
        elif key == arcade.key.J:
            self.shoot_pressed = False
        elif key == arcade.key.K:
            self.shoot_explosivo_pressed = False

        self.process_keychange()

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        # Guardamos el estado exacto del juego para poder volver a él
        self.game_view = game_view

    def on_draw(self):
        self.clear()
        
        #Dibujamos el juego congelado de fondo
        self.game_view.on_draw()

        #Activamos la cámara de la interfaz para dibujar sobre toda la pantalla
        self.game_view.gui_camera.use()

        #Ancho y alto de la pantalla actual
        ancho = self.window.width
        alto = self.window.height

        #Dibujamos un rectángulo negro semitransparente para oscurecer el juego
        arcade.draw_lrbt_rectangle_filled(
            left=0, right=ancho, top=alto, bottom=0,
            color=(0, 0, 0, 150) # El 150 es el nivel de transparencia (Alpha)
        )

        #Dibujamos los textos
        arcade.draw_text(
            "JUEGO EN PAUSA",
            ancho // 2,
            alto // 2 + 30,
            arcade.color.ORANGE_PEEL,
            font_size=50,
            font_name="Upheaval TT (BRK)",
            anchor_x="center"
        )
        arcade.draw_text(
            "Presiona ESC para continuar",
            ancho // 2,
            alto // 2 - 30,
            arcade.color.LIGHT_GRAY,
            font_size=20,
            font_name="Upheaval TT (BRK)",
            anchor_x="center"
        )
        arcade.draw_text(
            "Presiona ENTER para salir al Menú Principal",
            ancho // 2,
            alto // 2 - 70,
            arcade.color.LIGHT_GRAY,
            font_size=15,
            font_name="Upheaval TT (BRK)",
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        # Si presiona ESC, restauramos la vista del juego
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
            
        # Si presiona ENTER, destruimos el juego y volvemos al inicio
        elif key == arcade.key.ENTER:
            cts.PLAYING_LEVEL = False
            menu_view = mainMenu()
            self.window.show_view(menu_view)

def main():
    """Main function"""
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,resizable=True)
    
    window.MainMenuClass = mainMenu
    window.GameViewClass = GameView
    window.nivel_seleccionado = 1

    menu_view = mainMenu()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":

    # Obtenemos la ruta del proyecto utilizando PathLib,
    # necesitamos esta ruta para poder acceder a los archivos con recursos
    # de forma independiente desde donde se ejecute el script.
    PROJECT_ROOT = Path(__file__).parent.parent

    print(f"Project root is: {PROJECT_ROOT}")

    # Ejemplo de acceso a un archivo dentro de recursos
    filetest = PROJECT_ROOT / "assets" / "dialogs.txt"
    print(f"Test file size: {filetest.stat().st_size} bytes")
    
    main()