
import math
from pathlib import Path
import arcade
from constants import *


class Character(arcade.Sprite):
    def __init__(self, name_folder, name_file):
        super().__init__()

        self.facing_direction = RIGHT_FACING

        self.cur_texture = 0

        main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"
        # Load textures for idle, jump, and fall states
        idle_texture = arcade.load_texture(f"{main_path}_idle.png")
        jump_texture = arcade.load_texture(f"{main_path}_jump.png")
        fall_texture = arcade.load_texture(f"{main_path}_fall.png")
        # Make pairs with left and right facing textures
        self.idle_texture_pair = idle_texture, idle_texture.flip_left_right()
        self.jump_texture_pair = jump_texture, jump_texture.flip_left_right()
        self.fall_texture_pair = fall_texture, fall_texture.flip_left_right()
        # Load textures for walking with left and right facing textures
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture(f"{main_path}_walk{i}.png")
            self.walk_textures.append((texture, texture.flip_left_right()))

        self.climbing_textures = (
            arcade.load_texture(f"{main_path}_climb0.png"),
            arcade.load_texture(f"{main_path}_climb1.png")
        )

        # This variable will change dynamically and will represent the currently
        # active texture.
        self.texture = self.idle_texture_pair[0]


class PlayerCharacter(Character):
    def __init__(self):
        super().__init__("female_adventurer", "femaleAdventurer")

        # Track extra state related to the player. We will use these for change
        # textures in animations
        self.climbing = False
        self.should_update_walk = 0

    def update_animation(self, delta_time):

        # Figure out the direction the character is facing based on the movement
        # and previous direction.
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Handle animations for climbing on ladders. We use the absolute value
        # of change_y here because we don't care if the character is moving up
        # or down, the animation stays the same.
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Handling jumping animations
        if self.change_y > 0 and not self.climbing:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return
        elif self.change_y < 0 and not self.climbing:
            self.texture = self.fall_texture_pair[self.facing_direction]
            return

        # Handle idle animations
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Handle walking
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1


class Enemy(Character):
    def __init__(self, name_folder, name_file):
        super().__init__(name_folder, name_file)

        self.should_update_walk = 0

    def update_animation(self, delta_time):
        # Figure out the direction the character is facing based on the
        # movement and previous direction.
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Handle idle animations
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Handle walking
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1


class RobotEnemy(Enemy):
    def __init__(self):
        super().__init__("robot", "robot")
        self.health = 100


class ZombieEnemy(Enemy):
    def __init__(self):
        super().__init__("zombie", "zombie")
        self.health = 50