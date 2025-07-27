from loguru import logger

import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultObjectBuilder
from crunge.engine.d2.entity import StaticEntity2D
from crunge.engine.d2.sprite import Sprite, SpriteVu

class StaticObjectGroupBuilder(tiled_builder.DefaultObjectGroupBuilder):
    def __init__(self, context: tiled_builder.BuilderContext):
        def create_node_cb(position, rotation, scale, sprite, properties: dict):
            logger.debug(f"process_object: {position}, {sprite}, {properties}")
            node = StaticEntity2D(position, rotation, scale, vu=SpriteVu(), model=sprite)
            return node


        super().__init__(context, object_builder=DefaultObjectBuilder(context, create_node_cb=create_node_cb))
