from loguru import logger
import glm

from crunge.engine.d2.physics import PhysicsEngine2D

import badwing.globe
from badwing.constants import *
from badwing.assets import asset
from badwing.level import Level

from badwing.scene_layer import SceneLayer
from badwing.objects.barrier import BarrierLayer
from badwing.background import BackgroundLayer
from badwing.tile import TileLayer, TileFactory

from badwing.characters.factory import CharacterFactory

from badwing.objects.flag import FlagFactory
from badwing.characters.butterfly import ButterflyFactory

# from badwing.firework import Firework
from badwing.obstacle import ObstacleFactory

from ..effects.sparks import Sparks


class TileLevel(Level):
    def __init__(self, name: str, physics_engine: PhysicsEngine2D):
        super().__init__(name, physics_engine)

    def _create(self):
        super()._create()
        self.physics_engine.create()

        # --- Load in a map from the tiled editor ---

        self.barrier_layer = self.add_layer(BarrierLayer("barrier"))
        '''
        self.background_layer = self.add_layer(
            BackgroundLayer(
                "background", ":resources:/backgrounds/backgroundColorGrass.png"
            )
        )
        '''
        #self.scenery_layer = self.add_layer(TileLayer("scenery"))
        self.scenery_layer = self.get_layer("scenery")
        # self.ladder_layer = self.add_layer(TileLayer(self, "ladder"))
        self.ladder_layer = self.get_layer("ladder")
        logger.debug(f"ladder_layer: {self.ladder_layer}")
        self.flag_layer = self.add_layer(TileLayer("flags", FlagFactory))
        # self.ground_layer = self.add_layer(TileLayer("ground", TileFactory))
        self.ground_layer = self.get_layer("ground")
        logger.debug(f"ground_layer: {self.ground_layer}")
        self.spark_layer = self.add_layer(SceneLayer("spark"))
        # self.character_layer = self.add_layer(TileLayer(self, "pc", CharacterFactory))
        self.character_layer = self.get_layer("pc")
        logger.debug(f"character_layer: {self.character_layer}")
        """
        self.butterfly_layer = self.add_layer(
            TileLayer(self, "butterfly", ButterflyFactory)
        )
        """
        self.butterfly_layer = self.get_layer("butterfly")
        logger.debug(f"butterfly_layer: {self.butterfly_layer}")
        # self.obstacle_layer = self.add_layer(TileLayer(self, 'obstacle', ObstacleFactory))
        #self.object_layer = self.add_layer(TileLayer("object", ObstacleFactory))
        self.object_layer = self.get_layer("object")
        #self.static_layer = self.add_layer(TileLayer("static", TileFactory))
        self.static_layer = self.get_layer("static")

    """
    def check_butterflies(self):
        pass
    """

    def check_butterflies(self):
        hit_list = self.butterfly_layer.query_intersection(badwing.globe.avatar.bounds)
        for node in hit_list:
            if badwing.globe.player.collect(node):
                # Remove the butterfly
                node.destroy()
                self.spark_layer.attach(Sparks(node.position, glm.vec2(32, 32)))
                # self.spark_layer.add_effect(Firework(sprite.position))
                # arcade.play_sound(self.collect_butterfly_sound)

    """
    def check_butterflies(self):
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
    """

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
