from loguru import logger
import glm

from crunge.engine.d2.physics import PhysicsEngine2D

import badwing.globe
from badwing.constants import *
from badwing.level import Level

from badwing.scene_layer import SceneLayer
from badwing.objects.barrier import BarrierLayer
from badwing.background import BackgroundLayer
from badwing.tile import TileLayer

from ..effects.sparks import Sparks


class TileLevel(Level):
    def __init__(self, name: str, physics_engine: PhysicsEngine2D):
        super().__init__(name, physics_engine)

    def _create(self):
        super()._create()
        self.physics_engine.create()

        self.barrier_layer = self.add_layer(BarrierLayer("barrier"))

        self.scenery_layer = self.get_layer("scenery")
        self.ladder_layer = self.get_layer("ladder")
        self.flag_layer = self.get_layer("flags")
        self.ground_layer = self.get_layer("ground")
        self.spark_layer = self.add_layer(SceneLayer("spark"))
        self.character_layer = self.get_layer("pc")
        self.butterfly_layer = self.get_layer("butterfly")
        self.object_layer = self.get_layer("object")
        self.static_layer = self.get_layer("static")

    def check_butterflies(self):
        hit_list = self.butterfly_layer.query_intersection(badwing.globe.avatar.bounds)
        for node in hit_list:
            if badwing.globe.player.collect(node):
                # Remove the butterfly
                node.destroy()
                self.spark_layer.attach(Sparks(node.position))
                # arcade.play_sound(self.collect_butterfly_sound)

    def check_flags(self):
        hit_list = self.flag_layer.query_intersection(badwing.globe.avatar.bounds)
        for node in hit_list:
            if badwing.globe.player.collect(node):
                # Remove the flag
                node.destroy()
                self.spark_layer.attach(Sparks(node.position))
                # arcade.play_sound(self.collect_butterfly_sound)

    def check_collisions(self):
        self.check_butterflies()
        self.check_flags()
