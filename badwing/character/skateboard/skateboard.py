from loguru import logger
import glm

import crunge.box2d as box2d

from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.entity import EntityGroup2D, Entity2D, DynamicEntity2D
from crunge.engine.d2.physics import BoxGeom, BallGeom
from crunge.engine.d2.physics import globe as physics_globe

from ...util import debounce

from .skateboard_controller import SkateboardController

WHEEL_RADIUS = 0.25

CHASSIS_WIDTH = 0.5
CHASSIS_HEIGHT = 0.1

X_PAD = 0.3
Y_PAD = 0.25

SPEED_DELTA = 0.001
MAX_SPEED = 0.1

# No motor/torque constants any more - propulsion is direct velocity control
# (see update() below), same pattern DynamicCharacterController uses for
# _apply_ground_movement. Wheel joints stay motorless/free-spinning, which
# also removes the reaction-torque path that was causing the pitch wobble.

sprite_loader = SpriteLoader(sprite_builder=CollidableSpriteBuilder())


class Wheel(DynamicEntity2D):
    geom = BallGeom()

    def __init__(self, position=glm.vec2()):
        sprite = sprite_loader.load("${resources}/items/coinGold.png")
        scale = glm.vec2(0.5, 0.5)
        super().__init__(position, scale=scale, model=sprite)

    @classmethod
    def produce(self, position=glm.vec2()):
        return Wheel(position)


class Chassis(DynamicEntity2D):
    geom = BoxGeom()

    def __init__(self, position=glm.vec2()):
        sprite = sprite_loader.load("${resources}/tiles/boxCrate.png")

        scale = glm.vec2(1.5, 0.1)
        super().__init__(position, scale=scale, model=sprite)

    @classmethod
    def produce(self, position=glm.vec2()):
        return Chassis(position)


class Skateboard(EntityGroup2D):
    def __init__(self, position=glm.vec2()):
        super().__init__(position)
        self.mountee = None
        self.mountee_joints = []
        self.speed = 0

        chassis_pos = position
        front_wheel_pos = chassis_pos - glm.vec2(-(CHASSIS_WIDTH / 2 + X_PAD), Y_PAD)
        back_wheel_pos = chassis_pos - glm.vec2(CHASSIS_WIDTH / 2 + X_PAD, Y_PAD)

        self._front_wheel_pos = front_wheel_pos
        self._back_wheel_pos = back_wheel_pos

        self.chassis = self.add_node(Chassis.produce(chassis_pos))
        self.front_wheel = self.add_node(Wheel.produce(front_wheel_pos))
        self.back_wheel = self.add_node(Wheel.produce(back_wheel_pos))

    @property
    def velocity(self):
        return self.chassis.velocity

    @classmethod
    def produce(self, position=glm.vec2(0, 0)):
        return Skateboard(position)

    def control(self):
        return SkateboardController(self)

    def mount(self, mountee: Entity2D):
        self.mountee = mountee
        point = glm.vec2(0, 0.6)
        mountee.on_mount(self.chassis, point)
        logger.debug(f"mountee body: {mountee.body}")

        world = physics_globe.world

        mountee_anchor = box2d.Vec2(0, 0)
        mounted_anchor = box2d.Vec2(0, 0.6)
        weld_def = box2d.WeldJointDef(
            body_id_a=mountee.body,
            body_id_b=self.chassis.body,
            local_frame_a=box2d.Transform(p=mountee_anchor),
            local_frame_b=box2d.Transform(p=mounted_anchor),
        )
        weld_joint = box2d.create_weld_joint(world, weld_def)
        self.mountee_joints = [weld_joint]

    def dismount(self):
        logger.debug("dismounting")
        if self.mountee is None:
            return
        for joint_id in self.mountee_joints:
            box2d.destroy_joint(joint_id)
        self.mountee_joints = []
        point = glm.vec2(0, CHASSIS_HEIGHT / 2)
        self.mountee.on_dismount(self.chassis, point)
        self.mountee = None

    def _created(self):
        super()._created()

        world = physics_globe.world

        front_anchor_on_chassis = box2d.Vec2(
            *(self._front_wheel_pos - self.chassis.position)
        )
        back_anchor_on_chassis = box2d.Vec2(
            *(self._back_wheel_pos - self.chassis.position)
        )
        wheel_anchor = box2d.Vec2(0, 0)

        front_joint_def = box2d.RevoluteJointDef(
            body_id_a=self.front_wheel.body,
            body_id_b=self.chassis.body,
            local_frame_a=box2d.Transform(p=wheel_anchor),
            local_frame_b=box2d.Transform(p=front_anchor_on_chassis),
            enable_motor=False,  # free-spinning - propulsion applied directly to chassis velocity
        )

        back_joint_def = box2d.RevoluteJointDef(
            body_id_a=self.back_wheel.body,
            body_id_b=self.chassis.body,
            local_frame_a=box2d.Transform(p=wheel_anchor),
            local_frame_b=box2d.Transform(p=back_anchor_on_chassis),
            enable_motor=False,
        )

        self.front_joint = box2d.create_revolute_joint(world, front_joint_def)
        self.back_joint = box2d.create_revolute_joint(world, back_joint_def)

    def accelerate(self, rate=SPEED_DELTA):
        self.speed = min(self.speed + rate, MAX_SPEED)

    def decelerate(self, rate=SPEED_DELTA):
        self.speed = max(self.speed - rate, -MAX_SPEED)

    def coast(self):
        self.speed = 0

    @debounce(1)
    def ollie(self, impulse=(0, 1.0), point=(0, 0)):
        logger.debug("ollie")
        chassis_body = self.chassis.body
        chassis_world_point = chassis_body.get_world_point(
            box2d.Vec2(*point)
        )  # ASSUMPTION
        chassis_body.apply_linear_impulse(
            box2d.Vec2(*impulse), chassis_world_point, True
        )

        if self.mountee:
            mountee_body = self.mountee.body
            mountee_world_point = mountee_body.get_world_point(
                box2d.Vec2(*point)
            )  # ASSUMPTION
            mountee_body.apply_linear_impulse(
                box2d.Vec2(*impulse), mountee_world_point, True
            )

    def update(self, delta_time=1 / 60):
        super().update(delta_time)
        self._apply_propulsion()

    def _apply_propulsion(self):
        body = self.chassis.body
        angle = body.angle  # ASSUMPTION property name
        forward = glm.vec2(glm.cos(angle), glm.sin(angle))

        impulse_scale = self.speed
        impulse = forward * impulse_scale

        body.apply_linear_impulse_to_center(box2d.Vec2(impulse.x, impulse.y), True)
