import sys
import os

import arcade

import badwing.app
from badwing.constants import *
from badwing.assets import asset
import badwing.level

from badwing.physics.dynamic import DynamicPhysics
from badwing.physics.kinematic import KinematicPhysics
from badwing.layer import Layer
from badwing.barrier import BarrierLayer
from badwing.background import BackgroundLayer
from badwing.tile import TileLayer, StaticTileLayer
from badwing.ladder import LadderLayer
from badwing.skateboard import Wheel, Skateboard
from badwing.dude import Dude
from badwing.character import PlayerCharacter

from badwing.box import Box
from badwing.ball import Ball
from badwing.flag import FlagTileLayer
from badwing.butterfly import ButterflyTileLayer
from badwing.firework import Firework
from badwing.obstacle import ObstacleTileLayer
from badwing.debug import DebugLayer


class Level2(badwing.level.Level):
    def __init__(self):
        super().__init__('level2')

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        #self.physics_engine = physics_engine = KinematicPhysics(k_gravity=K_GRAVITY)
        self.physics_engine = physics_engine = DynamicPhysics()
        self.space = physics_engine.space

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Load sounds
        self.collect_butterfly_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.collect_flag_sound = arcade.load_sound(":resources:sounds/upgrade5.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        '''
        # Soundtrack
        self.album_title = album_title = 'original'
        self.song_title = song_title = 'eastin_trance'
        self.song = arcade.load_sound(asset(f'music/{album_title}/{song_title}.ogg'))
        '''
    @classmethod
    def create(self):
        level = Level2()
        level.setup()
        level.post_setup()
        return level

    #next level
    def get_next_level(self):
        import badwing.levels.end
        return badwing.levels.end.EndScreen

    def setup(self):
        super().setup()

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # --- Load in a map from the tiled editor ---

        # Name of map file to load
        map_name = asset("level2.tmx")
        # Name of the layer that has items for pick-up
        coins_layer_name = 'coins'

        self.add_layer(BarrierLayer(self, 'barrier'))
        self.add_layer(BackgroundLayer(self, 'background', ":resources:images/backgrounds/abstract_1.jpg"))
        self.ladder_layer = self.add_layer(LadderLayer(self, 'ladder'))
        self.flag_layer = flag_layer = self.add_animated_layer(FlagTileLayer(self, 'flags'))
        self.ground_layer = self.add_layer(StaticTileLayer(self, 'ground'))
        self.spark_layer = self.add_layer(Layer(self, 'spark'))
        self.player_layer = player_layer = self.add_layer(Layer(self, 'player'))
        self.butterfly_layer = self.add_animated_layer(ButterflyTileLayer(self, 'butterfly'))
        self.obstacle_layer = self.add_layer(ObstacleTileLayer(self, 'obstacle'))
        self.object_layer = self.add_layer(ObstacleTileLayer(self, 'object'))

        if DEBUG_COLLISION:
            self.debug_layer = debug_layer = self.add_layer(DebugLayer(self, 'debug'))
            self.debug_list = debug_layer.debug_list
        
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
        self.player_sprite = player.dude.sprite

        # --- Other stuff
        # Set the background color
        if self.map.background_color:
            arcade.set_background_color(self.background_color)

    def post_setup(self):
        super().post_setup()
        self.push_avatar(self.player.control())

    def check_butterflies(self):
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.butterfly_layer.sprites)
        for sprite in hit_list:
            model = sprite.model
            if badwing.app.player.collect(model):
                # Remove the butterfly
                sprite.remove_from_sprite_lists()
                self.spark_layer.add_effect(Firework(sprite.position))
                arcade.play_sound(self.collect_butterfly_sound)

    def check_flags(self):
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.flag_layer.sprites)
        for sprite in hit_list:
            model = sprite.model
            if badwing.app.player.collect(model):
                self.spark_layer.add_effect(Firework(sprite.position, 60, 100))
                arcade.play_sound(self.collect_flag_sound)

    def check_collisions(self):
        self.check_butterflies()
        self.check_flags()

    def update(self, delta_time):
        super().update(delta_time)
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
            # Clamp the viewport to the level boundaries
            (vp_left, vp_right, vp_bottom, vp_top) = viewport = arcade.get_viewport()
            low_bottom = self.bottom
            high_bottom = self.top - (vp_top - vp_bottom)
            low_left = self.left
            high_left = self.right - (vp_right - vp_left)
            
            self.view_bottom = int(arcade.clamp(self.view_bottom, low_bottom, high_bottom))

            self.view_left = int(arcade.clamp(self.view_left, low_left, high_left))

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def draw(self):
        super().draw()
        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {badwing.app.player.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)
