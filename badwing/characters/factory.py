from loguru import logger
import glm

from badwing.characters import Avatar
from badwing.characters import Skateboard

# from badwing.characters import Blob
# from badwing.characters import Skeleton
from badwing.characters import Robot

#from badwing.model_factory import ModelFactory


class CharacterFactory(ModelFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def process_object(self, position: glm.vec2, image, properties):
        logger.debug(f"process_object: {position}, {image}, {properties}")
        # kind = properties.get('class')
        kind = properties.get("type")
        if not kind:
            return
        node = kinds[kind].produce(position)
        print(node)
        self.layer.attach(node)


kinds = {
    "PlayerCharacter": Avatar,
    "Skateboard": Skateboard,
    "Robot": Robot,
    # "hero": PlayerCharacter,
    #'blob': Blob,
    #'enemy': Skeleton,
    #'skeleton': Skeleton,
}
