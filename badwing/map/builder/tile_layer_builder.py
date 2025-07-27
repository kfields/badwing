import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultTileBuilder
from crunge.engine.d2.sprite import SpriteVu

from ...tile import Tile

class TileLayerBuilder(tiled_builder.DefaultTileLayerBuilder):
    def __init__(self, context: tiled_builder.BuilderContext):
        def create_node_cb(position, sprite, properties: dict):
            return Tile(position, SpriteVu(), sprite)

        super().__init__(context, tile_builder=DefaultTileBuilder(context, create_node_cb=create_node_cb))