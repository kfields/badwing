from loguru import logger
import glm
import pymunk

from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.entity import PhysicsGroup2D, DynamicEntity2D
from crunge.engine.d2.physics import BoxGeom, BallGeom
import crunge.engine.d2.physics.globe as physics_globe

from badwing.util import debounce

from .skateboard_controller import SkateboardController


WHEEL_RADIUS = 32
WHEEL_MASS = 5

# CHASSIS_WIDTH = 128
CHASSIS_WIDTH = 64
CHASSIS_HEIGHT = 16
#CHASSIS_MASS = 1
#CHASSIS_MASS = 10
CHASSIS_MASS = 2
# X_PAD = 32
X_PAD = 48
# Y_PAD = 32
Y_PAD = 28

SPEED_DELTA = 1
MAX_SPEED = 100

sprite_loader = SpriteLoader(sprite_builder=CollidableSpriteBuilder())


class Wheel(DynamicEntity2D):
    def __init__(self, position=glm.vec2()):
        sprite = sprite_loader.load(":resources:/items/coinGold.png")
        scale = glm.vec2(0.5, 0.5)
        super().__init__(
            position, scale=scale, vu=SpriteVu(), model=sprite, geom=BallGeom()
        )
        self.mass = WHEEL_MASS

    @classmethod
    def produce(self, position=glm.vec2()):
        return Wheel(position)


class Chassis(DynamicEntity2D):
    def __init__(self, position=glm.vec2()):
        sprite = sprite_loader.load(":resources:/tiles/boxCrate.png")

        scale = glm.vec2(1.5, 0.1)
        super().__init__(
            position, scale=scale, vu=SpriteVu(), model=sprite, geom=BoxGeom()
        )
        self.mass = CHASSIS_MASS

    @classmethod
    def produce(self, position=glm.vec2()):
        return Chassis(position)


class Skateboard(PhysicsGroup2D):
    def __init__(self, position=glm.vec2()):
        super().__init__(position)
        self.mountee = None
        self.mountee_pins = []
        self.speed = 0
        self.motors_attached = True

        chassis_pos = position
        front_wheel_pos = chassis_pos - glm.vec2(-(CHASSIS_WIDTH / 2 + X_PAD), Y_PAD)
        back_wheel_pos = chassis_pos - glm.vec2(CHASSIS_WIDTH / 2 + X_PAD, Y_PAD)

        self.chassis = chassis = self.add_node(Chassis.produce(chassis_pos))
        self.vu = chassis.vu
        self.front_wheel = self.add_node(Wheel.produce(front_wheel_pos))
        self.back_wheel = self.add_node(Wheel.produce(back_wheel_pos))

    @property
    def velocity(self):
        return self.chassis.velocity

    @classmethod
    def produce(self, position=(0, 0)):
        return Skateboard(position)

    def control(self):
        return SkateboardController(self)

    def mount(self, mountee):
        self.mountee = mountee
        point = glm.vec2(0, 16)
        mountee.on_mount(self.chassis, point)
        logger.debug(f"mountee body: {mountee.body}")

        p5 = pymunk.PinJoint(mountee.body, self.chassis.body, (-16, 32), tuple(point))
        p6 = pymunk.PinJoint(mountee.body, self.chassis.body, (16, 32), tuple(point))

        self.mountee_pins.extend([p5, p6])

        physics_globe.physics_engine.space.add(p5, p6)

    def dismount(self):
        logger.debug("dismounting")
        if self.mountee is None:
            return
        physics_globe.physics_engine.space.remove(*self.mountee_pins)
        self.mountee_pins = []
        point = glm.vec2(0, CHASSIS_HEIGHT / 2)
        self.mountee.on_dismount(self.chassis, point)
        self.mountee = None

    def _create(self):
        super()._create()

        p1 = pymunk.PinJoint(
            self.back_wheel.body, self.chassis.body, (0, 0), (-CHASSIS_WIDTH / 2, 0)
        )
        p2 = pymunk.PinJoint(
            self.back_wheel.body, self.chassis.body, (0, 0), (0, -CHASSIS_HEIGHT / 2)
        )
        p3 = pymunk.PinJoint(
            self.front_wheel.body, self.chassis.body, (0, 0), (CHASSIS_WIDTH / 2, 0)
        )
        p4 = pymunk.PinJoint(
            self.front_wheel.body, self.chassis.body, (0, 0), (0, -CHASSIS_HEIGHT / 2)
        )

        self.front_motor = m1 = pymunk.constraints.SimpleMotor(
            self.front_wheel.body, self.chassis.body, -self.speed
        )
        m1.max_force = 200000
        self.back_motor = self.motor = m2 = pymunk.constraints.SimpleMotor(
            self.back_wheel.body, self.chassis.body, -self.speed
        )
        m2.max_force = 200000

        physics_globe.physics_engine.space.add(p1, p2, p3, p4, m1, m2)

    def attach_motors(self):
        if self.motors_attached:
            return
        self.front_motor.rate = self.back_motor.rate = -self.speed
        physics_globe.physics_engine.space.add(self.back_motor, self.front_motor)
        self.motors_attached = True

    def detach_motors(self):
        if not self.motors_attached:
            return
        physics_globe.physics_engine.space.remove(self.back_motor, self.front_motor)
        self.motors_attached = False

    def accelerate(self, rate=SPEED_DELTA):
        speed = self.speed + rate
        if speed > MAX_SPEED:
            return
        self.speed = speed
        if not self.motors_attached:
            self.attach_motors()

    def decelerate(self, rate=SPEED_DELTA):
        speed = self.speed - rate
        if speed < -MAX_SPEED:
            return
        self.speed = speed
        if not self.motors_attached:
            self.attach_motors()

    def coast(self):
        self.detach_motors()
        self.speed = 0

    @debounce(1)
    def ollie(self, impulse=(0, 4000), point=(0, 0)):
        logger.debug("ollie")
        # self.chassis.body.apply_impulse_at_local_point(impulse, point)
        self.mountee.body.apply_impulse_at_local_point(impulse, point)

    def update(self, delta_time=1 / 60):
        super().update(delta_time)
        if self.motors_attached:
            self.front_motor.rate = self.back_motor.rate = -self.speed
