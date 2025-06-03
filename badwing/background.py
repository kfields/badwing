from crunge.engine.d2.background import BackgroundVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.builder.sprite.background_sprite_builder import BackgroundSpriteBuilder

from badwing.constants import *
from badwing.tile import TileLayer

class BackgroundLayer(TileLayer):
    def __init__(self, name, filename):
        super().__init__(name)
        self.filename = filename
        self.background = None
        
    def _create(self):
        super()._create()
        sprite = self.sprite = SpriteLoader(sprite_builder=BackgroundSpriteBuilder()).load(":resources:/backgrounds/backgroundColorGrass.png")
        node = self.node = Node2D(vu=BackgroundVu(), model=sprite)
        self.attach(node)

