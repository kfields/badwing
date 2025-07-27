import glm
from pytmx import TiledTileLayer

from crunge.engine.math import Bounds2

from crunge.engine.loader.tiled.builder import BuilderContext
from crunge.engine.loader.tiled.builder.tile_builder import (
    TileBuilder,
    DefaultTileBuilder,
)

from crunge.engine.loader.tiled.builder.tile_layer_builder import TileLayerBuilder
from badwing.background import BackgroundLayer


class BackgroundLayerBuilder(TileLayerBuilder):
    def __init__(self, context: BuilderContext, tile_builder: TileBuilder = None):
        super().__init__(
            context,
            tile_builder if tile_builder is not None else DefaultTileBuilder(context),
        )

    def build(self, layer: TiledTileLayer, layer_id: int):
        scene_layer = BackgroundLayer(
            "background", ":resources:/backgrounds/backgroundColorGrass.png"
        )

        size = self.context.size
        scene_layer.bounds = Bounds2(0, 0, size.x, size.y)
        self.context.layer = scene_layer
        super().build(layer, layer_id)
        self.context.scene.add_layer(self.context.layer)
