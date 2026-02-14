from loguru import logger

import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultTileBuilder

from ...objects.flag import Pole, Flag


class FlagLayerBuilder(tiled_builder.DefaultTileLayerBuilder):
    def __init__(self):
        def create_node_cb(position, sprite, properties: dict):
            logger.debug(f"process_object: {position}, {sprite}, {properties}")
            # kind = properties.get('class')
            kind = properties.get("type")
            if not kind:
                logger.debug(f"kind not found: {kind}")
                return

            if kind == 'Pole':
                node = Pole(position, sprite)
            else:
                node = Flag.produce(kind, position, sprite)


            logger.debug(f"node: {node}")
            return node

        super().__init__(
            tile_builder=DefaultTileBuilder(create_node_cb=create_node_cb),
        )
