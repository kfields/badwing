import sys
import os

import arcade

import badwing.level
from badwing.constants import *
from badwing.physics.dynamic import DynamicPhysicsEngine
from badwing.physics.kinematic import KinematicPhysicsEngine
from badwing.layer import Layer, BackgroundLayer
from badwing.tile import TileLayer, StaticTileLayer
from badwing.ladder import LadderLayer
from badwing.skateboard import Wheel, Skateboard
from badwing.dude import Dude
from badwing.character import PlayerCharacter

from badwing.box import Box
from badwing.ball import Ball
from badwing.butterfly import ButterflyLayer
from badwing.emitter import EmitterLayer
from badwing.obstacle import ObstacleLayer

class Level(badwing.level.Level):
    def __init__(self):
        super().__init__('level1')

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        #self.physics_engine = physics_engine = KinematicPhysicsEngine(k_gravity=K_GRAVITY)
        self.physics_engine = physics_engine = DynamicPhysicsEngine()
        self.space = physics_engine.space

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

        # --- Load in a map from the tiled editor ---

        # Name of map file to load
        map_name = "assets/map/level1.tmx"
        # Name of the layer that has items for pick-up
        coins_layer_name = 'coins'

        self.add_layer(BackgroundLayer(self, 'background', ":resources:images/backgrounds/abstract_1.jpg"))
        self.ladder_layer = self.add_layer(LadderLayer(self, 'ladder'))
        self.ground_layer = self.add_layer(StaticTileLayer(self, 'ground'))
        self.spark_layer = self.add_layer(EmitterLayer(self, 'spark'))
        self.player_layer = player_layer = self.add_layer(Layer(self, 'player'))
        self.butterfly_layer = self.add_layer(ButterflyLayer(self, 'butterfly'))
        self.obstacle_layer = self.add_layer(ObstacleLayer(self, 'obstacle'))
        
        # player_layer.add_model(Box.create())
        
        '''
        player = Dude.create()
        player_layer.add_model(player)
        '''
        '''
        player = PlayerCharacter.create()
        player_layer.add_model(player)
        '''
        
        player = Skateboard.create(position=(392, 192))
        player_layer.add_model(player)
        
        self.player = player
        self.player_sprite = player.sprite

        # --- Other stuff
        # Set the background color
        if self.map.background_color:
            arcade.set_background_color(self.background_color)

        self.post_setup()

    def post_setup(self):
        super().post_setup()
        print(self.ground_layer.sprites)
        # Create the 'physics engine'
        '''
        self.physics_engine.setup(self.player_sprite,
                                    self.ground_layer.sprites,
                                    self.ladder_layer.sprites
                                    )
        '''
        # Requires physics engine to exist first
        self.player.control()

    def update(self, delta_time):
        super().update(delta_time)
        """ Movement and game logic """
        # Move the player with the physics engine
        self.physics_engine.update()

        self.player_layer.update_animation(delta_time)
        self.butterfly_layer.update_animation(delta_time)

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.butterfly_layer.sprites)

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            self.spark_layer.make_sparks(coin.position)
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

    def draw(self):
        super().draw()
        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)
