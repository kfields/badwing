from crunge.engine.loader.tiled import TiledMapLoader, SceneBuilderContext
from .builder.map_builder import MapBuilder
from ..scene import Scene

class MapLoader(TiledMapLoader):
    def __init__(self, scene: Scene):
        context = SceneBuilderContext(scene)
        super().__init__(context, map_builder=MapBuilder(context))
