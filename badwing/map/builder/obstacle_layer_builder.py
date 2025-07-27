from loguru import logger

import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultTileBuilder

from ...obstacle import Obstacle


class ObstacleLayerBuilder(tiled_builder.DefaultTileLayerBuilder):
    def __init__(self, context: tiled_builder.BuilderContext):
        def create_node_cb(position, sprite, properties: dict):
            logger.debug(f"create_node_cb: {position}, {sprite}, {properties}")
            kind = properties.get("type")
            if not kind:
                logger.debug(f"kind not found: {kind}")
                return
            node = Obstacle.produce(kind, position, sprite)

            logger.debug(f"node: {node}")
            return node

        super().__init__(
            context,
            tile_builder=DefaultTileBuilder(context, create_node_cb=create_node_cb),
        )
