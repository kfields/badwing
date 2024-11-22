from loguru import logger
import glm

from badwing.characters import PlayerCharacter
from badwing.characters import Skateboard

# from badwing.characters import Blob
# from badwing.characters import Skeleton
from badwing.characters import Robot

from badwing.model_factory import ModelFactory


class CharacterFactory(ModelFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def process_object(self, position: glm.vec2, image, properties):
        logger.debug(f"process_object: {position}, {image}, {properties}")
        # kind = properties.get('class')
        kind = properties.get("type")
        if not kind:
            return
        model = kinds[kind].produce(position)
        print(model)
        self.layer.add_model(model)


kinds = {
    "PlayerCharacter": PlayerCharacter,
    "Skateboard": Skateboard,
    "Robot": Robot,
    # "hero": PlayerCharacter,
    #'blob': Blob,
    #'enemy': Skeleton,
    #'skeleton': Skeleton,
}
