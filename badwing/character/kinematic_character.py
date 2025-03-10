from loguru import logger
import glm

from crunge.engine.d2.entity import PhysicsEntity2D, KinematicEntity2D
from crunge.engine.d2.physics import (
    KinematicPhysics,
    DynamicPhysics,
    HullGeom,
)

from crunge.engine.d2.sprite import SpriteVu

from badwing.constants import *
import badwing.globe

from badwing.character.controller import KinematicCharacterController

PLAYER_MASS = 1


class KinematicCharacter(KinematicEntity2D):
    def __init__(self, position=glm.vec2(), vu=SpriteVu(), model=None, brain=None):
        super().__init__(position, vu=vu, model=model, brain=brain, geom=HullGeom())
        self.mass = PLAYER_MASS

    def on_mount(self, node: PhysicsEntity2D, point: glm.vec2):
        # super().on_mount(point)
        self.mounted = True
        self.position = node.get_tx_point(
            glm.vec2(point.x, point.y + self.height / 2)
        )
        logger.debug(f"mounting at {self.position}")
        self.angle = node.angle
        # print('on_mount')
        #self.physics = DynamicPhysics()
        self.physics = DynamicPhysics(glm.vec2(0, -self.height / 2))
        logger.debug(f"shapes: {self.shapes}")

    def on_dismount(self, node: PhysicsEntity2D, point: glm.vec2):
        # super().on_dismount(point)
        self.mounted = False
        self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2))
        #self.position = glm.vec2(node.position[0], node.position[1] + self.height / 2)
        # self.angle = model.angle
        self.angle = 0
        self.physics = KinematicPhysics()
        badwing.globe.screen.pop_avatar()

    """
    @classmethod
    def produce(self, position=glm.vec2()):
        #vu = CharacterVu().create()
        vu = SpriteVu()
        brain = CharacterBrain()
        return KinematicCharacter(position, vu=vu, brain=brain)
    """

    def control(self):
        return KinematicCharacterController(self)