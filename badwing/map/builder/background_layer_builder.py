from pytmx import TiledImageLayer

from crunge.engine.math import Bounds2

from crunge.engine.loader.tiled.builder import BuilderContext

from crunge.engine.loader.tiled.builder.image_layer_builder import ImageLayerBuilder
from badwing.background import BackgroundLayer


class BackgroundLayerBuilder(ImageLayerBuilder):
    def __init__(self, context: BuilderContext):
        super().__init__(context)

    def build(self, layer: TiledImageLayer, layer_id: int):
        path = layer.source
        scene_layer = BackgroundLayer(
            "background", path
        )

        size = self.context.size
        scene_layer.bounds = Bounds2(0, 0, size.x, size.y)
        self.context.layer = scene_layer
        super().build(layer, layer_id)
        self.context.scene.add_layer(self.context.layer)
