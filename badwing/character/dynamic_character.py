from loguru import logger
import glm

from crunge import box2d as b2

from crunge.engine.math import Rect2

from crunge.engine.d2.entity import PhysicsEntity2D, DynamicEntity2D
from crunge.engine.d2.physics import HullGeom
from crunge.engine.d2.physics import MotionState

from crunge.engine.d2.sprite import Sprite, SpriteVu

from ..constants import *
from ..collision_type import CollisionType
from .. import globe

from ..character.controller import DynamicCharacterController

PLAYER_MASS = 70
FOOT_FRICTION = 1.2


class DynamicCharacter(DynamicEntity2D):
    model: Sprite

    def __init__(self, position=glm.vec2(), vu=SpriteVu(), model=None, brain=None):
        super().__init__(position, vu=vu, model=model, brain=brain, geom=HullGeom())
        self.mass = PLAYER_MASS
        self.mass_data: b2.MassData = None
        self.feet_shape: b2.Shape = None

    def _create(self):
        super()._create()
        self.lock_rotation()

    def create_shapes(self, clip: Rect2 = None):
        x = -(self.width / 2)
        y = 0
        width = self.width
        height = self.height / 2
        clip = Rect2(x, y, width, height)
        logger.debug(f"clip: {clip}")
        super().create_shapes(clip=clip)
        self._create_feet_shape()

    def _create_feet_shape(self):
        # avatar.body is a b2BodyId (see PPU/Box2D migration notes:
        # geometry is authored in meters at creation time).
        body = self.body
        size = self.size
        hh = size.y / 2
        logger.debug(
            f"creating feet shape for {self} at body {body}, size: {size}, half-height: {hh}"
        )

        feet_y = -hh + 0.25

        circle = b2.Circle()
        circle.center = b2.Vec2(0.0, feet_y)
        circle.radius = 0.25

        shape_def = b2.ShapeDef()
        shape_def.material = b2.SurfaceMaterial(friction=FOOT_FRICTION, restitution=0.0)

        shape_def.is_sensor = False  # feet still need contact response; only
        # the *ground layer* would be a sensor
        shape_def.enable_contact_events = True  # required on BOTH shapes

        self.feet_shape = b2.create_circle_shape(body, shape_def, circle)
        self.feet_shape.user_data = self
        self.feet_shape.user_material = CollisionType.FEET

        # Ground/other shapes in this pair must also opt in:
        # enableContactEvents = True is needed on the *other* shape too,
        # wherever ground/kinematic shapes are created.

    def lock_rotation(self):
        self.body.set_motion_locks(b2.MotionLocks(False, False, True))

    def unlock_rotation(self):
        self.body.set_motion_locks(b2.MotionLocks(False, False, False))

    def on_mount(self, node: PhysicsEntity2D, point: glm.vec2):
        logger.debug(f"mounting: node={node}, point={point}")
        self.motion_state = MotionState.MOUNTED
        self.unlock_rotation()
        logger.debug(f"mounting at {self.position}")

        self.mass_data = self.body.mass_data
        mass_data = self.body.mass_data

        logger.debug(
            f"mass data: mass={mass_data.mass}, center={mass_data.center}, inertia={mass_data.rotational_inertia}"
        )
        mass_data.mass = 0.1
        com = mass_data.center
        mass_data.center = b2.Vec2(com.x, com.y - 1)
        self.body.mass_data = mass_data

    def on_dismount(self, node: PhysicsEntity2D, point: glm.vec2):
        logger.debug(f"dismounting from {node}")
        self.motion_state = MotionState.FALLING
        self.lock_rotation()
        self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2))
        self.angle = 0

        logger.debug(
            f"mass data: mass={self.mass_data.mass}, center={self.mass_data.center}, inertia={self.mass_data.rotational_inertia}"
        )
        self.body.mass_data = self.mass_data

        logger.debug(
            f"applied mass data: mass={self.body.mass_data.mass}, center={self.body.mass_data.center}, inertia={self.body.mass_data.rotational_inertia}"
        )
        self.body.linear_velocity = b2.Vec2(0, 0)
        self.body.set_transform(b2.Vec2(*self.position), b2.make_rot(0))
        self.lock_rotation()  # Re-lock rotation
        globe.screen.pop_avatar()

    def control(self):
        return DynamicCharacterController(self)
