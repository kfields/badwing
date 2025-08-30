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
    def __init__(self, context: tiled_builder.BuilderContext):
        super().__init__(context)
        self.add_image_layer_builder("background", BackgroundLayerBuilder(context))
        self.add_tile_layer_builder("ground", TileLayerBuilder(context))
        self.add_object_group_builder("pc", CharacterLayerBuilder(context))
        self.add_tile_layer_builder("butterfly", ButterflyLayerBuilder(context))
        self.add_object_group_builder("static", StaticObjectGroupBuilder(context))
        self.add_object_group_builder("object", DynamicObjectGroupBuilder(context))
        self.add_tile_layer_builder("obstacle", ObstacleLayerBuilder(context))
        self.add_tile_layer_builder("flags", FlagLayerBuilder(context))
