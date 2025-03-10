from loguru import logger

import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultObjectBuilder

from badwing.characters import Avatar
from badwing.characters import Skateboard

# from badwing.characters import Blob
# from badwing.characters import Skeleton
from badwing.characters import Robot

from ...tile import Tile

class CharacterLayerBuilder(tiled_builder.DefaultObjectGroupBuilder):
    def __init__(self, context: tiled_builder.SceneBuilderContext):
        def create_node_cb(position, rotation, sprite, properties: dict):
            logger.debug(f"process_object: {position}, {sprite}, {properties}")
            kind = properties.get("type")
            if not kind:
                logger.debug(f"kind not found: {kind}")
                return
            node = kinds[kind].produce(position)
            logger.debug(f"node: {node}")
            return node


        super().__init__(context, object_builder=DefaultObjectBuilder(context, create_node_cb=create_node_cb))

kinds = {
    "PlayerCharacter": Avatar,
    "Skateboard": Skateboard,
    "Robot": Robot,
    # "hero": PlayerCharacter,
    #'blob': Blob,
    #'enemy': Skeleton,
    #'skeleton': Skeleton,
}
