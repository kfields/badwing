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


class TileLevel(Level):
    def __init__(self, name: str, physics_engine: PhysicsEngine2D):
        super().__init__(name, physics_engine)

    def _create(self):
        super()._create()
        self.physics_engine.create()

        # --- Load in a map from the tiled editor ---

        self.add_layer(BarrierLayer(self, "barrier"))
        self.add_layer(
            BackgroundLayer(
                self, "background", ":resources:/backgrounds/backgroundColorGrass.png"
            )
        )
        self.scenery_layer = self.add_layer(TileLayer(self, "scenery"))
        #self.ladder_layer = self.add_layer(TileLayer(self, "ladder"))
        self.ladder_layer = self.get_layer("ladder")
        self.flag_layer = self.add_layer(TileLayer(self, "flags", FlagFactory))
        self.ground_layer = self.add_layer(TileLayer(self, "ground", TileFactory))
        #self.ground_layer = self.get_layer("ground")
        self.spark_layer = self.add_layer(SceneLayer(self, "spark"))
        #self.character_layer = self.add_layer(TileLayer(self, "pc", CharacterFactory))
        self.character_layer = self.get_layer("pc")
        '''
        self.butterfly_layer = self.add_layer(
            TileLayer(self, "butterfly", ButterflyFactory)
        )
        '''
        self.butterfly_layer = self.get_layer("butterfly")
        # self.obstacle_layer = self.add_layer(TileLayer(self, 'obstacle', ObstacleFactory))
        self.object_layer = self.add_layer(TileLayer(self, "object", ObstacleFactory))
        self.static_layer = self.add_layer(TileLayer(self, "static", TileFactory))

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
