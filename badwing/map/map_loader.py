from crunge.engine.loader.tiled import TiledMapLoader, SceneBuilderContext


class MapLoader(TiledMapLoader):
    def __init__(self):
        context = SceneBuilderContext()
        super().__init__(context)
