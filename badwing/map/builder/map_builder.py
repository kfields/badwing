import crunge.engine.loader.tiled.builder as tiled_builder

from .tile_layer_builder import TileLayerBuilder
from .background_layer_builder import BackgroundLayerBuilder
from .character_layer_builder import CharacterLayerBuilder
from .butterfly_layer_builder import ButterflyLayerBuilder
from .static_object_group_builder import StaticObjectGroupBuilder
from .dynamic_object_group_builder import DynamicObjectGroupBuilder
from .obstacle_layer_builder import ObstacleLayerBuilder
from .flag_layer_builder import FlagLayerBuilder

class MapBuilder(tiled_builder.DefaultMapBuilder):
    def __init__(self):
        super().__init__()
        self.add_image_layer_builder("background", BackgroundLayerBuilder())
        self.add_tile_layer_builder("ground", TileLayerBuilder())
        self.add_object_group_builder("pc", CharacterLayerBuilder())
        self.add_tile_layer_builder("butterfly", ButterflyLayerBuilder())
        self.add_object_group_builder("static", StaticObjectGroupBuilder())
        self.add_object_group_builder("object", DynamicObjectGroupBuilder())
        self.add_tile_layer_builder("obstacle", ObstacleLayerBuilder())
        self.add_tile_layer_builder("flags", FlagLayerBuilder())
