import math
import glm
import pymunk
from pymunk import Vec2d
import arcade

import badwing.app
from badwing.constants import *
from badwing.assets import asset
from badwing.util import debounce
from badwing.character import CharacterAvatar
from badwing.model import DynamicModel, Group


WHEEL_RADIUS = 32
WHEEL_MASS = .5

CHASSIS_WIDTH = 128
CHASSIS_HEIGHT = 16
CHASSIS_MASS = 1

X_PAD = 32
Y_PAD = 32

SPEED_DELTA = 1
MAX_SPEED = 100

class Wheel(DynamicModel):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)
        self.position = position

    @classmethod
    def create(self, position=(0,0)):
        img_src = asset("items/coinGold.png")
        sprite = arcade.Sprite(img_src, CHARACTER_SCALING)
        return Wheel(sprite, position)

    def on_add(self, layer):
        super().on_add(layer)
        layer.add_sprite(self.sprite)

    def create_body(self):
        #print(self.position)
        mass = WHEEL_MASS
        radius = WHEEL_RADIUS
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self.body = body = pymunk.Body(mass, inertia)
        body.position = self.position

    def create_shapes(self):
        print('wheel')
        radius = WHEEL_RADIUS
        shape = pymunk.Circle(self.body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        shape.filter = pymunk.ShapeFilter(self.gid)
        self.shapes.append(shape)


class Chassis(DynamicModel):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)
        self.position = position

    @classmethod
    def create(self, position=(192, 192)):
        img_src = asset("tiles/boxCrate.png")
        sprite = arcade.Sprite(img_src, CHARACTER_SCALING)
        sprite.width = TILE_WIDTH * TILE_SCALING * 2
        sprite.height = CHASSIS_HEIGHT * TILE_SCALING
        return Chassis(sprite, position)

    def on_add(self, layer):
        super().on_add(layer)
        layer.add_sprite(self.sprite)

    def create_body(self):
        print('body')
        position = self.position
        width = CHASSIS_WIDTH * TILE_SCALING
        height = CHASSIS_HEIGHT * TILE_SCALING

        mass = CHASSIS_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        self.body = body = pymunk.Body(mass, moment)
        body.position = position

    def create_shapes(self):
        width = CHASSIS_WIDTH * TILE_SCALING
        height = CHASSIS_HEIGHT * TILE_SCALING

        shape = pymunk.Poly.create_box(self.body, (width, height))
        shape.friction = 10
        shape.elasticity = 0.2
        shape.filter = pymunk.ShapeFilter(self.gid)
        self.shapes.append(shape)


class Skateboard(Group):
    def __init__(self, position=(292, 192)):
        super().__init__()
        self.position = position
        self.mountee = None
        self.mountee_pins = []
        self.speed = 0
        self.motors_attached = True

        chassis_pos = Vec2d(position)
        front_wheel_pos = chassis_pos - (-(CHASSIS_WIDTH/2+X_PAD), Y_PAD)
        back_wheel_pos = chassis_pos - (CHASSIS_WIDTH/2+X_PAD, Y_PAD)

        self.chassis = chassis = self.add_model(Chassis.create(chassis_pos))
        self.sprite = chassis.sprite
        self.front_wheel = front_wheel = self.add_model(Wheel.create(front_wheel_pos))
        self.back_wheel = back_wheel = self.add_model(Wheel.create(back_wheel_pos))

    @classmethod
    def create(self, position=(292, 192)):
        return Skateboard(position)

    def control(self):
        return SkateboardAvatar(self)

    def mount(self, mountee):
        self.mountee = mountee
        position = self.chassis.body.position + (0, CHASSIS_HEIGHT/2+Y_PAD*2)
        mountee.on_mount(position)
        p5 = pymunk.PinJoint(mountee.body, self.chassis.body, (0,0), (CHASSIS_WIDTH/2,0))
        p6 = pymunk.PinJoint(mountee.body, self.chassis.body, (0,0), (0,CHASSIS_HEIGHT/2))
        self.mountee_pins.extend([p5, p6])
        badwing.app.physics_engine.space.add(p5, p6)

    def dismount(self):
        badwing.app.physics_engine.space.remove(self.mountee_pins)
        self.mountee_pins = []
        position = self.chassis.body.position + (0, CHASSIS_HEIGHT/2+Y_PAD*2)
        self.mountee.on_dismount(position)

    def on_add(self, layer):
        super().on_add(layer)
        position = self.position
        '''
        layer.add_model(self.chassis)
        layer.add_model(self.front_wheel)
        layer.add_model(self.back_wheel)
        '''
        p1 = pymunk.PinJoint(self.back_wheel.body, self.chassis.body, (0,0), (-CHASSIS_WIDTH/2,0))
        p2 = pymunk.PinJoint(self.back_wheel.body, self.chassis.body, (0,0), (0,-CHASSIS_HEIGHT/2))
        p3 = pymunk.PinJoint(self.front_wheel.body, self.chassis.body, (0,0), (CHASSIS_WIDTH/2,0))
        p4 = pymunk.PinJoint(self.front_wheel.body, self.chassis.body, (0,0), (0,-CHASSIS_HEIGHT/2))

        self.front_motor = m1 = pymunk.constraint.SimpleMotor(self.front_wheel.body, self.chassis.body, -self.speed)
        m1.max_force = 200000
        self.back_motor = self.motor = m2 = pymunk.constraint.SimpleMotor(self.back_wheel.body, self.chassis.body, -self.speed)
        m2.max_force = 200000

        badwing.app.physics_engine.space.add(p1, p2, p3, p4, m1, m2)

    def attach_motors(self):
        if self.motors_attached:
            return
        self.front_motor.rate = self.back_motor.rate = -self.speed
        badwing.app.physics_engine.space.add(self.back_motor, self.front_motor)
        self.motors_attached = True

    def detach_motors(self):
        if not self.motors_attached:
            return
        badwing.app.physics_engine.space.remove(self.back_motor, self.front_motor)
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

class SkateboardAvatar(CharacterAvatar):
    def __init__(self, skateboard):
        super().__init__(skateboard)
        self.skateboard = skateboard

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.skateboard.ollie()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.skateboard.dismount()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_down = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_down = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_down = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_down = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_down = False

    def update(self, delta_time):
        if self.left_down:
            self.skateboard.decelerate()
        elif self.right_down:
            self.skateboard.accelerate()
        else:
            self.skateboard.coast()
