from loguru import logger

from crunge.engine.d2.physics import PhysicsEngine2D
from crunge.engine.d2.graph_layer_2d import GraphLayer2D

from .. import globe
from ..level import Level

from ..objects.barrier import BarrierLayer

from ..effects.sparks import Sparks


class TileLevel(Level):
    def __init__(self, name: str, physics_engine: PhysicsEngine2D):
        super().__init__(name, physics_engine)

    def _create(self):
        super()._create()
        self.physics_engine.create()
        # TODO: Replace these attributes with a more dynamic layer management system
        # EXAMPLE:
        # scenery_layer = self.get_layer(SceneryLayer) #???
        # Only that would mean creating a layer class for each type of layer, which might be overkill for now
        # Of course, I think I actually coded a way to dynamically create classes (Look at the Layer class in "Deeper"!!!)

        self.scenery_layer = self.get_layer("scenery")
        self.ladder_layer = self.get_layer("ladder")
        self.flag_layer = self.get_layer("flags")
        self.ground_layer = self.get_layer("ground")
        self.character_layer = self.get_layer("pc")
        self.butterfly_layer = self.get_layer("butterfly")
        self.object_layer = self.get_layer("object")
        self.static_layer = self.get_layer("static")

        self.barrier_layer = self.add_layer(BarrierLayer("barrier"))
        self.spark_layer = self.add_layer(GraphLayer2D("spark"))

    def check_butterflies(self):
        hit_list = self.butterfly_layer.query_intersection(globe.avatar.bounds)
        for node in hit_list:
            if globe.player.collect(node):
                # Remove the butterfly
                node.destroy()
                self.spark_layer.attach(Sparks(node.position))
                # arcade.play_sound(self.collect_butterfly_sound)

    def check_flags(self):
        hit_list = self.flag_layer.query_intersection(globe.avatar.bounds)
        for node in hit_list:
            if globe.player.collect(node):
                # Remove the flag
                node.destroy()
                self.spark_layer.attach(Sparks(node.position))
                # arcade.play_sound(self.collect_butterfly_sound)

    def check_collisions(self):
        self.check_butterflies()
        self.check_flags()
