from loguru import logger
import glm
import pymunk

from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder

from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.entity import PhysicsEntity2D, PhysicsGroup2D, DynamicEntity2D
from crunge.engine.d2.physics import BoxGeom, BallGeom
import crunge.engine.d2.physics.globe as physics_globe

from badwing.assets import asset
from badwing.util import debounce

from .skateboard_controller import SkateboardController


WHEEL_RADIUS = 32
#WHEEL_MASS = .5
WHEEL_MASS = 5

#CHASSIS_WIDTH = 128
CHASSIS_WIDTH = 64
CHASSIS_HEIGHT = 16
#CHASSIS_MASS = 1
CHASSIS_MASS = 2

X_PAD = 32
Y_PAD = 32

SPEED_DELTA = 1
MAX_SPEED = 100

sprite_loader = SpriteLoader(sprite_builder=CollidableSpriteBuilder())

class Wheel(DynamicEntity2D):
    def __init__(self, position=glm.vec2()):
        img_src = asset("items/coinGold.png")
        sprite = sprite_loader.load(img_src)
        vu = SpriteVu(sprite).create()
        size = glm.vec2(WHEEL_RADIUS, WHEEL_RADIUS)
        scale = glm.vec2(.5, .5)
        super().__init__(position, size=size, scale=scale, vu=vu, model=sprite, geom=BallGeom())
        #super().__init__(position, scale=scale, vu=vu, model=sprite, geom=BallGeom())
        self.size = self.size * .5
        #self.radius = WHEEL_RADIUS
        self.mass = WHEEL_MASS

    @classmethod
    def produce(self, position=glm.vec2()):
        return Wheel(position)

'''
class Wheel(DynamicEntity2D):
    def __init__(self, position=glm.vec2(), vu=None):
        super().__init__(position, vu=vu, geom=BallGeom())
        #self.radius = WHEEL_RADIUS
        self.mass = WHEEL_MASS

    @classmethod
    def produce(self, position=(0,0)):
        img_src = asset("items/coinGold.png")
        sprite = sprite_loader.load(img_src)
        vu = SpriteVu(sprite).create()

        return Wheel(position, vu)
'''

class Chassis(DynamicEntity2D):
    def __init__(self, position=glm.vec2()):
        img_src = asset("tiles/boxCrate.png")
        sprite = sprite_loader.load(img_src)
        vu = SpriteVu(sprite).create()

        size = glm.vec2(CHASSIS_WIDTH, CHASSIS_HEIGHT)
        scale = glm.vec2(1.5, .1)
        super().__init__(position, size=size, scale=scale, vu=vu, model=sprite, geom=BoxGeom())
        #self.size = self.size
        self.width = CHASSIS_WIDTH
        self.height = CHASSIS_HEIGHT
        self.mass = CHASSIS_MASS

    @classmethod
    def produce(self, position=glm.vec2()):
        return Chassis(position)

'''
class Chassis(DynamicEntity2D):
    def __init__(self, position=glm.vec2(), vu=None):
        size = glm.vec2(CHASSIS_WIDTH, CHASSIS_HEIGHT)
        super().__init__(position, size=size, vu=vu, geom=BoxGeom())
        #self.width = CHASSIS_WIDTH
        #self.height = CHASSIS_HEIGHT
        self.mass = CHASSIS_MASS

    @classmethod
    def produce(self, position=(0, 0)):
        img_src = asset("tiles/boxCrate.png")
        #sprite.width = TILE_WIDTH * TILE_SCALING * 2
        #sprite.height = CHASSIS_HEIGHT * TILE_SCALING
        sprite = sprite_loader.load(img_src)
        vu = SpriteVu(sprite).create()

        return Chassis(position, vu)
'''

class Skateboard(PhysicsGroup2D):
    def __init__(self, position=glm.vec2()):
        super().__init__(position)
        self.mountee = None
        self.mountee_pins = []
        self.speed = 0
        self.motors_attached = True

        chassis_pos = position
        front_wheel_pos = chassis_pos - glm.vec2(-(CHASSIS_WIDTH/2+X_PAD), Y_PAD)
        back_wheel_pos = chassis_pos - glm.vec2(CHASSIS_WIDTH/2+X_PAD, Y_PAD)

        self.chassis = chassis = self.add_node(Chassis.produce(chassis_pos))
        self.vu = chassis.vu
        self.front_wheel = self.add_node(Wheel.produce(front_wheel_pos))
        self.back_wheel = self.add_node(Wheel.produce(back_wheel_pos))

    @classmethod
    def produce(self, position=(0,0)):
        return Skateboard(position)

    def control(self):
        return SkateboardController(self)

    def mount(self, mountee):
        self.mountee = mountee
        mount_width = self.chassis.width
        mount_height = self.chassis.height

        point = glm.vec2(0, CHASSIS_HEIGHT/2)
        mountee.on_mount(self.chassis, point)
        logger.debug(f"mountee body: {mountee.body}")

        p5 = pymunk.PinJoint(mountee.body, self.chassis.body, (0,0), (0,CHASSIS_HEIGHT/2))
        p6 = pymunk.PinJoint(mountee.body, self.chassis.body, (0,0), (0,CHASSIS_HEIGHT/2))
        '''
        p5 = pymunk.PinJoint(mountee.body, self.chassis.body, (0,0))
        p6 = pymunk.PinJoint(mountee.body, self.chassis.body, (0,0))
        '''
        self.mountee_pins.extend([p5, p6])

        physics_globe.physics_engine.space.add(p5, p6)

    def dismount(self):
        physics_globe.physics_engine.space.remove(*self.mountee_pins)
        self.mountee_pins = []
        point = glm.vec2(0, CHASSIS_HEIGHT/2)
        self.mountee.on_dismount(self.chassis, point)

    def _create(self):
        super()._create()

        p1 = pymunk.PinJoint(self.back_wheel.body, self.chassis.body, (0,0), (-CHASSIS_WIDTH/2,0))
        p2 = pymunk.PinJoint(self.back_wheel.body, self.chassis.body, (0,0), (0,-CHASSIS_HEIGHT/2))
        p3 = pymunk.PinJoint(self.front_wheel.body, self.chassis.body, (0,0), (CHASSIS_WIDTH/2,0))
        p4 = pymunk.PinJoint(self.front_wheel.body, self.chassis.body, (0,0), (0,-CHASSIS_HEIGHT/2))

        self.front_motor = m1 = pymunk.constraints.SimpleMotor(self.front_wheel.body, self.chassis.body, -self.speed)
        m1.max_force = 200000
        self.back_motor = self.motor = m2 = pymunk.constraints.SimpleMotor(self.back_wheel.body, self.chassis.body, -self.speed)
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
    def ollie(self, impulse=(0,2000), point=(0,0)):
        self.chassis.body.apply_impulse_at_local_point(impulse, point)

    def update(self, delta_time=1/60):
        super().update(delta_time)
        if self.motors_attached:
            self.front_motor.rate = self.back_motor.rate = -self.speed
