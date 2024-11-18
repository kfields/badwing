import sys
import os

import arcade

import badwing.app
from badwing.constants import *
from badwing.assets import asset

from badwing.physics.dynamic import DynamicPhysicsEngine
from badwing.physics.kinematic import KinematicPhysicsEngine
from badwing.layer import Layer
from badwing.barrier import BarrierLayer
from badwing.background import BackgroundLayer

from badwing.tile import TileLayer, TileFactory 

from badwing.characters.factory import CharacterFactory
from badwing.characters import PlayerCharacter

from badwing.flag import FlagFactory
from badwing.characters.butterfly import ButterflyFactory
from badwing.firework import Firework
from badwing.obstacle import ObstacleFactory
from badwing.debug import DebugLayer
from badwing.coin import CoinFactory

from badwing.level import StickerLevel

class Sandbox(StickerLevel):
    @classmethod
    def produce(self):
        level = Sandbox('sandbox')
        level.create()
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

        self.add_layer(BarrierLayer(self, 'barrier'))

        self.parallax_layer = self.add_layer(TileLayer(self, 'parallax'))

        self.background_layer = self.add_layer(TileLayer(self, 'background'))

        self.ground_layer = self.add_layer(TileLayer(self, 'ground', TileFactory))

        self.ground_layer = self.add_layer(TileLayer(self, 'foreground'))

        self.castle_layer = self.add_layer(TileLayer(self, 'castle'))

        self.castledeco_layer = self.add_layer(TileLayer(self, 'castledeco'))

        self.shading_layer = self.add_layer(TileLayer(self, 'shading'))

        #self.light_layer = self.add_layer(TileLayer(self, 'light'))
        self.light_layer = None

        self.obstacle_layer = self.add_layer(TileLayer(self, 'obstacle', ObstacleFactory))

        #self.flag_layer = flag_layer = self.add_animated_layer(TileLayer(self, 'flags', FlagFactory))
        self.flag_layer = None

        #self.ladder_layer = self.add_layer(TileLayer(self, 'ladder'))
        self.ladder_layer = None

        self.coin_layer = coin_layer = self.add_layer(TileLayer(self, 'coin', CoinFactory))

        #self.butterfly_layer = self.add_animated_layer(TileLayer(self, 'butterfly', ButterflyFactory))

        self.spark_layer = self.add_layer(Layer(self, 'spark'))

        self.character_layer = character_layer = self.add_animated_layer(TileLayer(self, 'game', CharacterFactory))

        self.above_layer = self.add_layer(TileLayer(self, 'above'))
                
        # --- Other stuff
        # Set the background color
        if self.map.background_color:
            arcade.set_background_color(self.map.background_color)

        self.physics_engine.create()
