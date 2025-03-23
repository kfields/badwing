from loguru import logger
import glm

from badwing.characters import Avatar
from badwing.characters import Skateboard

# from badwing.characters import Blob
# from badwing.characters import Skeleton
from badwing.characters import Robot


kinds = {
    "PlayerCharacter": Avatar,
    "Skateboard": Skateboard,
    "Robot": Robot,
    # "hero": PlayerCharacter,
    #'blob': Blob,
    #'enemy': Skeleton,
    #'skeleton': Skeleton,
}
