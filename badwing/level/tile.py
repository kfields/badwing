import sys
import os

import arcade

import badwing.app
from badwing.constants import *
from badwing.assets import asset
from badwing.level import Level

from badwing.physics.dynamic import DynamicPhysicsEngine
from badwing.physics.kinematic import KinematicPhysicsEngine
from badwing.layer import Layer
from badwing.barrier import BarrierLayer
from badwing.background import BackgroundLayer
from badwing.tile import TileLayer, TileFactory

#from badwing.character import CharacterTileLayer
from badwing.characters.factory import CharacterFactory
from badwing.characters import PlayerCharacter, Skateboard, Chassis

from badwing.flag import FlagFactory
from badwing.characters.butterfly import ButterflyFactory
from badwing.firework import Firework
from badwing.obstacle import ObstacleFactory
from badwing.debug import DebugLayer

class TileLevel(Level):
    def __init__(self, name):
        super().__init__(name)

        # Our physics engine
        self.physics_engine = physics_engine = KinematicPhysicsEngine()
        #self.physics_engine = physics_engine = DynamicPhysicsEngine()
        self.space = physics_engine.space

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Load sounds
        self.collect_butterfly_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.collect_flag_sound = arcade.load_sound(":resources:sounds/upgrade5.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        # Soundtrack
        self.song = arcade.load_sound(asset('music/funkyrobot.ogg'))

    @classmethod
    def create(self):
        level = Level1()
        level.setup()
        return level
        
    #next level
    def get_next_level(self):
        import badwing.scenes.level2
        return badwing.scenes.level2.Level2

    def do_setup(self):
        super().do_setup()

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # --- Load in a map from the tiled editor ---

        self.add_layer(BarrierLayer(self, 'barrier'))
        self.add_layer(BackgroundLayer(self, 'background', ":resources:images/backgrounds/abstract_1.jpg"))
        self.scenery_layer = self.add_layer(TileLayer(self, 'scenery'))
        self.ladder_layer = self.add_layer(TileLayer(self, 'ladder'))
        self.flag_layer = flag_layer = self.add_animated_layer(TileLayer(self, 'flags', FlagFactory))
        self.ground_layer = self.add_layer(TileLayer(self, 'ground', TileFactory))
        self.spark_layer = self.add_layer(Layer(self, 'spark'))
        self.character_layer = character_layer = self.add_animated_layer(TileLayer(self, 'pc', CharacterFactory))
        self.butterfly_layer = self.add_animated_layer(TileLayer(self, 'butterfly', ButterflyFactory))
        self.obstacle_layer = self.add_layer(TileLayer(self, 'obstacle', ObstacleFactory))
        self.object_layer = self.add_layer(TileLayer(self, 'object', ObstacleFactory))
        self.static_layer = self.add_layer(TileLayer(self, 'static', TileFactory))
                
        # character_layer.add_model(Box.create())
        
        # --- Other stuff
        # Set the background color
        if self.map.background_color:
            arcade.set_background_color(self.map.background_color)

        self.physics_engine.setup()

    def post_setup(self):
        super().post_setup()
        pc = None
        for model in self.character_layer.models:
            if isinstance(model, PlayerCharacter):
                pc = model
                break
        self.push_pc(pc)

    def check_butterflies(self):
        hit_list = arcade.check_for_collision_with_list(self.pc_sprite, self.butterfly_layer.sprites)
        for sprite in hit_list:
            model = sprite.model
            if badwing.app.player.collect(model):
                # Remove the butterfly
                sprite.remove_from_sprite_lists()
                self.spark_layer.add_effect(Firework(sprite.position))
                arcade.play_sound(self.collect_butterfly_sound)

    def check_flags(self):
        hit_list = arcade.check_for_collision_with_list(self.pc_sprite, self.flag_layer.sprites)
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
        if self.pc_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.pc_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.pc_sprite.right > right_boundary:
            self.view_left += self.pc_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.pc_sprite.top > top_boundary:
            self.view_bottom += self.pc_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.pc_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.pc_sprite.bottom
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
