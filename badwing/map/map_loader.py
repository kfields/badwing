from crunge.engine.loader.tiled import TiledMapLoader, BuilderContext
from .builder.map_builder import MapBuilder
from ..scene import Scene

class MapLoader(TiledMapLoader):
    def __init__(self, scene: Scene):
        context = BuilderContext(scene)
        super().__init__(context, map_builder=MapBuilder())
