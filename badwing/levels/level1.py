import sys
import os

import arcade
import pymunk

from badwing.constants import *
import badwing.level
from badwing.layer import Layer
from badwing.tile import PhysicsTileLayer
from badwing.bike import Wheel, Bike
from badwing.ball import Ball

class Level(badwing.level.Level):
    def __init__(self):
        super().__init__('level1')
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = GRAVITY

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        super().setup()
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        #self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        #self.player_sprite = PlayerCharacter()
        #self.player_sprite.center_x = 256
        #self.player_sprite.center_y = 512
        #self.player_list.append(self.player_sprite)

        # --- Load in a map from the tiled editor ---

        # Name of map file to load
        map_name = "assets/map/level1.tmx"
        # Name of the layer that has items for pick-up
        coins_layer_name = 'coins'

        self.add_layer(PhysicsTileLayer(self, 'ground'))
        player_layer = self.add_layer(Layer(self, 'player'))

        bike = Bike.create()
        player_layer.add_model(bike)
        self.player_sprite = bike.chassis.sprite
        # --- Other stuff
        # Set the background color
        if self.map.background_color:
            arcade.set_background_color(self.background_color)

    def update(self, dt):
        super().update(dt)
        """ Movement and game logic """

        # Move the player with the physics engine
        #self.physics_engine.update()

        # self.player_list.update()
        self.player_list.update_animation()

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
