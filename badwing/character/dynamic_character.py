from loguru import logger
import glm

from crunge.engine.d2.entity import PhysicsEntity2D, DynamicEntity2D
from crunge.engine.d2.physics import (
    KinematicPhysics,
    DynamicPhysics,
    HullGeom,
)
from crunge.engine.d2.physics.physics import MotionState

from crunge.engine.d2.sprite import SpriteVu

from badwing.constants import *
import badwing.globe

from badwing.character.controller import DynamicCharacterController

PLAYER_MASS = 1


class DynamicCharacter(DynamicEntity2D):
    def __init__(self, position=glm.vec2(), vu=SpriteVu(), model=None, brain=None):
        super().__init__(position, vu=vu, model=model, brain=brain, geom=HullGeom())
        self.mass = PLAYER_MASS

    def on_mount(self, node: PhysicsEntity2D, point: glm.vec2):
        self.motion_state = MotionState.MOUNTED
        self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2 + 4))
        logger.debug(f"mounting at {self.position}")
        self.angle = node.angle
        # logger.debug('on_mount')
        #self.physics = DynamicPhysics(glm.vec2(0, -self.height / 2))
        logger.debug(f"shapes: {self.shapes}")

    def on_dismount(self, node: PhysicsEntity2D, point: glm.vec2):
        self.motion_state = MotionState.FALLING
        self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2))
        self.angle = 0
        self.body.velocity = (0, 0)
        #self.physics = KinematicPhysics()
        badwing.globe.screen.pop_avatar()

    def control(self):
        return DynamicCharacterController(self)
