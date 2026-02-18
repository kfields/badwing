from loguru import logger
import glm

from crunge.engine.d2.entity import PhysicsEntity2D, DynamicEntity2D
from crunge.engine.d2.physics import HullGeom
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
        self.saved_moment = float('inf')

    def _create(self):
        super()._create()
        self.save_moment()
        self.lock_rotation()

    def save_moment(self):
        self.saved_moment = self.body.moment

    def restore_moment(self):
        self.body.moment = self.saved_moment

    def lock_rotation(self):
        self.body.moment = float('inf')

    def on_mount(self, node: PhysicsEntity2D, point: glm.vec2):
        self.restore_moment()
        self.motion_state = MotionState.MOUNTED
        self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2 + 4))
        logger.debug(f"mounting at {self.position}")
        self.angle = node.angle
        # logger.debug('on_mount')
        logger.debug(f"shapes: {self.shapes}")

    def on_dismount(self, node: PhysicsEntity2D, point: glm.vec2):
        self.motion_state = MotionState.FALLING
        self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2))
        self.angle = 0
        self.body.velocity = (0, 0)
        self.body.angle = 0
        self.body.angular_velocity = 0 # Stop any residual spin
        self.lock_rotation() # Re-lock rotation
        badwing.globe.screen.pop_avatar()

    def control(self):
        return DynamicCharacterController(self)
