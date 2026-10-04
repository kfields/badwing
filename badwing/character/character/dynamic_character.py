from loguru import logger
import glm

from crunge import box2d as b2

from crunge.engine.math import Rect2

from crunge.engine.d2.entity import PhysicsEntity2D, DynamicEntity2D
from crunge.engine.d2.physics import MotionState
from crunge.engine.d2.physics.geom import CompoundGeom, HullGeom, BallGeom

from crunge.engine.d2.sprite import Sprite, SpriteVu

from ... import globe
from ...physics_material import PLAYER, FEET

from .controller import DynamicCharacterController

FOOT_RADIUS = 0.25
MOUNTED_MASS = 0.1
MOUNTED_COM_DROP = 1.0


class DynamicCharacter(DynamicEntity2D):
    model: Sprite
    material = PLAYER
    geom = CompoundGeom([
        HullGeom(clip=Rect2(0, 0.5, 1.0, 0.5)),
        BallGeom(
            radius=FOOT_RADIUS,
            offset=glm.vec2(0, -FOOT_RADIUS),
            material=FEET,
        ),
    ])

    def __init__(self, position=None, model=None):
        super().__init__(position, model=model)
        self.mass_data: b2.MassData = None
        #self.add_chip(DynamicCharacterController(self))

    '''
    def _seat(self):
        super()._seat()
        self.add_chip(DynamicCharacterController(self))
    '''

    def _create(self):
        super()._create()
        self.physics.lock_rotation()

    def on_mount(self, node: PhysicsEntity2D, point: glm.vec2):
        self.motion_state = MotionState.MOUNTED
        self.physics.unlock_rotation()

        body = self.physics.body
        saved = body.mass_data
        self.mass_data = b2.MassData(
            mass=saved.mass,
            center=b2.Vec2(saved.center.x, saved.center.y),
            rotational_inertia=saved.rotational_inertia,
        )

        mounted = body.mass_data
        mounted.mass = MOUNTED_MASS
        mounted.center = b2.Vec2(
            mounted.center.x, mounted.center.y - MOUNTED_COM_DROP
        )
        body.mass_data = mounted

    def on_dismount(self, node: PhysicsEntity2D, point: glm.vec2):
        self.motion_state = MotionState.FALLING

        body = self.physics.body
        self.position = node.physics.get_tx_point(
            glm.vec2(point.x, point.y + self.height / 2)
        )
        self.rotation = 0
        body.set_transform(b2.Vec2(*self.position), b2.make_rot(0))

        if self.mass_data is not None:
            body.mass_data = self.mass_data
            self.mass_data = None
        body.linear_velocity = b2.Vec2(0, 0)
        self.physics.lock_rotation()
        globe.screen.pop_avatar()
