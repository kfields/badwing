from loguru import logger
import glm

from crunge.engine.d2.entity import PhysicsEntity2D, KinematicEntity2D
from crunge.engine.d2.physics import (
    KinematicPhysics,
    DynamicPhysics,
    HullGeom,
)
from crunge.engine.d2.physics import MotionState

from crunge.engine.d2.sprite import SpriteVu

from ...constants import *
from ... import globe

from .controller import KinematicCharacterController

PLAYER_MASS = 1


class KinematicCharacter(KinematicEntity2D):
    def __init__(self, position=glm.vec2(), vu=SpriteVu(), model=None, brain=None):
        super().__init__(position, vu=vu, model=model, brain=brain, geom=HullGeom())
        self.mass = PLAYER_MASS

    def on_mount(self, node: PhysicsEntity2D, point: glm.vec2):
        self.motion_state = MotionState.MOUNTED
        self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2 + 4))
        logger.debug(f"mounting at {self.position}")
        self.rotation = node.rotation
        # logger.debug('on_mount')
        self.physics = DynamicPhysics(glm.vec2(0, -self.height / 2))
        logger.debug(f"shapes: {self.shapes}")

    def on_dismount(self, node: PhysicsEntity2D, point: glm.vec2):
        self.motion_state = MotionState.FALLING
        self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2))
        self.rotation = 0
        self.body.linear_velocity = (0, 0)
        self.physics = KinematicPhysics()
        globe.screen.pop_avatar()

    def control(self):
        return KinematicCharacterController(self)
