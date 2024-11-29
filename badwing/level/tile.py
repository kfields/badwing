import sys
import os
import glm

from crunge.engine.d2.physics import KinematicPhysicsEngine, DynamicPhysicsEngine
from crunge.engine.d2.physics.draw_options import DrawOptions

import badwing.globe
from badwing.constants import *
from badwing.assets import asset
from badwing.level import Level

from badwing.scene_layer import SceneLayer
from badwing.objects.barrier import BarrierLayer
from badwing.background import BackgroundLayer
from badwing.tile import TileLayer, TileFactory

from badwing.characters.factory import CharacterFactory
from badwing.characters import PlayerCharacter, Skateboard, Chassis

from badwing.objects.flag import FlagFactory
from badwing.characters.butterfly import ButterflyFactory

# from badwing.firework import Firework
from badwing.obstacle import ObstacleFactory


class TileLevel(Level):
    def __init__(self, name):
        super().__init__(name)
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

    def _create(self):
        super()._create()

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0


        # self.physics_engine = physics_engine = KinematicPhysicsEngine(draw_options=self.draw_options)
        self.physics_engine = physics_engine = KinematicPhysicsEngine()
        # self.physics_engine = physics_engine = DynamicPhysicsEngine(draw_options=self.draw_options)
        self.space = physics_engine.space

        self.physics_engine.create()

        # --- Load in a map from the tiled editor ---

        self.add_layer(BarrierLayer(self, "barrier"))
        self.add_layer(
            BackgroundLayer(
                self, "background", ":resources:/backgrounds/backgroundColorGrass.png"
            )
        )
        self.scenery_layer = self.add_layer(TileLayer(self, "scenery"))
        self.ladder_layer = self.add_layer(TileLayer(self, "ladder"))
        self.flag_layer = self.add_layer(TileLayer(self, "flags", FlagFactory))
        self.ground_layer = self.add_layer(TileLayer(self, "ground", TileFactory))
        self.spark_layer = self.add_layer(SceneLayer(self, "spark"))
        self.character_layer = self.add_layer(TileLayer(self, "pc", CharacterFactory))
        self.butterfly_layer = self.add_layer(
            TileLayer(self, "butterfly", ButterflyFactory)
        )
        # self.obstacle_layer = self.add_layer(TileLayer(self, 'obstacle', ObstacleFactory))
        self.object_layer = self.add_layer(TileLayer(self, "object", ObstacleFactory))
        self.static_layer = self.add_layer(TileLayer(self, "static", TileFactory))

    def _post_create(self):
        super()._post_create()
        avatar = None
        for node in self.character_layer.root.children:
            if isinstance(node, PlayerCharacter):
                avatar = node
                break
        self.push_avatar(avatar)

    def check_butterflies(self):
        return
        hit_list = arcade.check_for_collision_with_list(
            self.pc_sprite, self.butterfly_layer.sprites
        )
        for sprite in hit_list:
            model = sprite.model
            if badwing.globe.player.collect(model):
                # Remove the butterfly
                sprite.remove_from_sprite_lists()
                self.spark_layer.add_effect(Firework(sprite.position))
                arcade.play_sound(self.collect_butterfly_sound)

    def check_flags(self):
        return
        hit_list = arcade.check_for_collision_with_list(
            self.pc_sprite, self.flag_layer.sprites
        )
        for sprite in hit_list:
            model = sprite.model
            if badwing.globe.player.collect(model):
                self.spark_layer.add_effect(Firework(sprite.position, 60, 100))
                arcade.play_sound(self.collect_flag_sound)

    def check_collisions(self):
        self.check_butterflies()
        self.check_flags()

    def update(self, delta_time: float):
        super().update(delta_time)
        # --- Manage Scrolling ---
        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.avatar.bounds.left < left_boundary:
            self.view_left -= left_boundary - self.avatar.bounds.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.avatar.bounds.right > right_boundary:
            self.view_left += self.avatar.bounds.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.avatar.bounds.top > top_boundary:
            self.view_bottom += self.avatar.bounds.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.avatar.bounds.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.avatar.bounds.bottom
            changed = True

        if changed:
            pass
            # self.camera.position = self.pc.position
            # self.camera.position = glm.lerp(self.camera.position, self.pc.position, delta_time)

    def draw(self, renderer):
        # self.physics_engine.debug_draw(renderer)
        super().draw(renderer)
