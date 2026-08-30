from loguru import logger
import glm

from badwing.character import Avatar
from badwing.character import Skateboard

# from badwing.characters import Blob
# from badwing.characters import Skeleton
from badwing.character import Robot


kinds = {
    "PlayerCharacter": Avatar,
    "Skateboard": Skateboard,
    "Robot": Robot,
    # "hero": PlayerCharacter,
    #'blob': Blob,
    #'enemy': Skeleton,
    #'skeleton': Skeleton,
}
