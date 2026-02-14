import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultTileBuilder
from crunge.engine.d2.sprite import SpriteVu

from ...tile import Tile

class TileLayerBuilder(tiled_builder.DefaultTileLayerBuilder):
    def __init__(self):
        def create_node_cb(position, sprite, properties: dict):
            return Tile(position, SpriteVu(), sprite)

        super().__init__(tile_builder=DefaultTileBuilder(create_node_cb=create_node_cb))