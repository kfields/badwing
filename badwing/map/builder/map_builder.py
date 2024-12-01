import crunge.engine.loader.tiled.builder as tiled_builder

from .tile_layer_builder import TileLayerBuilder
from .character_layer_builder import CharacterLayerBuilder
from .butterfly_layer_builder import ButterflyLayerBuilder

class MapBuilder(tiled_builder.DefaultMapBuilder):
    def __init__(self, context: tiled_builder.SceneBuilderContext):
        super().__init__(context)
        self.add_tile_layer_builder("ground", TileLayerBuilder(context))
        self.add_object_group_builder("pc", CharacterLayerBuilder(context))
        self.add_tile_layer_builder("butterfly", ButterflyLayerBuilder(context))