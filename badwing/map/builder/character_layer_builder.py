from loguru import logger

import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultObjectBuilder

from badwing.characters import Avatar
from badwing.characters import Skateboard

# from badwing.characters import Blob
# from badwing.characters import Skeleton
from badwing.characters import Robot


class CharacterLayerBuilder(tiled_builder.DefaultObjectGroupBuilder):
    def __init__(self):
        def create_node_cb(position, rotation, scale, sprite, properties: dict):
            logger.debug(f"CharacterLayerBuilder.create_node_cb: {position}, {sprite}, {properties}")
            kind = properties.get("type")
            if not kind:
                logger.debug(f"kind not found: {kind}")
                return
            node = kinds[kind].produce(position)
            logger.debug(f"Created node of kind {kind}: {node}")
            logger.debug(f"node: {node}")
            return node


        super().__init__(object_builder=DefaultObjectBuilder(create_node_cb=create_node_cb))

kinds = {
    "PlayerCharacter": Avatar,
    "Skateboard": Skateboard,
    "Robot": Robot,
    # "hero": PlayerCharacter,
    #'blob': Blob,
    #'enemy': Skeleton,
    #'skeleton': Skeleton,
}
