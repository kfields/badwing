from pytmx import TiledImageLayer

from crunge.engine.math import Bounds2

from crunge.engine.loader.tiled.builder.image_layer_builder import ImageLayerBuilder
from badwing.background import BackgroundLayer


class BackgroundLayerBuilder(ImageLayerBuilder):
    def build(self, tmx_layer: TiledImageLayer):
        path = tmx_layer.get_image_path()
        layer = BackgroundLayer(
            "background", path
        )

        size = self.context.size
        layer.bounds = Bounds2(0, 0, size.x, size.y)
        self.context.layer = layer
        super().build(tmx_layer)
        self.context.scene.add_layer(self.context.layer)
