import math
import glm
import pymunk
from pymunk import Vec2d
import arcade

import badwing.app
from badwing.constants import *
from badwing.assets import asset
from badwing.util import debounce
import badwing.avatar
from badwing.model import DynamicModel, Assembly
from badwing.dude import Dude


WHEEL_RADIUS = 32
WHEEL_MASS = 1

CHASSIS_WIDTH = 128
CHASSIS_HEIGHT = 32
CHASSIS_MASS = 1

X_PAD = 32
Y_PAD = 32

SPEED_DELTA = 1

class Wheel(DynamicModel):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)
        mass = WHEEL_MASS
        radius = WHEEL_RADIUS
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self.body = body = pymunk.Body(mass, inertia)
        body.position = position

        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        self.shapes.append(shape)

    @classmethod
    def create(self, position=(0,0)):
        img_src = asset("items/coinGold.png")
        sprite = arcade.Sprite(img_src, CHARACTER_SCALING)
        return Wheel(sprite, position)

    def on_add(self, layer):
        super().on_add(layer)
        layer.add_sprite(self.sprite)


class Chassis(DynamicModel):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)

        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        mass = CHASSIS_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        self.body = body = pymunk.Body(mass, moment)
        body.position = position

        shape = pymunk.Poly.create_box(body, (width, height))
        shape.friction = 10
        shape.elasticity = 0.2
        self.shapes.append(shape)

    @classmethod
    def create(self, position=(192, 192)):
        img_src = asset("tiles/boxCrate.png")
        sprite = arcade.Sprite(img_src, CHARACTER_SCALING, image_width=CHASSIS_WIDTH, image_height=CHASSIS_HEIGHT)
        return Chassis(sprite, position)

    def on_add(self, layer):
        super().on_add(layer)
        layer.add_sprite(self.sprite)


class Skateboard(Assembly):
    def __init__(self, position=(292, 192)):
        super().__init__()
        self.speed = 0
        self.motors_attached = True

        chassis_pos = Vec2d(position)
        back_wheel_pos = chassis_pos - (CHASSIS_WIDTH/2+X_PAD, Y_PAD)
        front_wheel_pos = chassis_pos - (-(CHASSIS_WIDTH/2+X_PAD), Y_PAD)
        dude_pos = chassis_pos + (0, CHASSIS_HEIGHT/2+Y_PAD*2)

        self.back_wheel = back_wheel = Wheel.create(back_wheel_pos)
        self.chassis = chassis = Chassis.create(chassis_pos)
        self.sprite = chassis.sprite
        self.dude = dude = Dude.create(dude_pos)
        self.front_wheel = front_wheel = Wheel.create(front_wheel_pos)

        p1 = pymunk.PinJoint(back_wheel.body, chassis.body, (0,0), (-CHASSIS_WIDTH/2,0))
        p2 = pymunk.PinJoint(back_wheel.body, chassis.body, (0,0), (0,-CHASSIS_HEIGHT/2))
        p3 = pymunk.PinJoint(front_wheel.body, chassis.body, (0,0), (CHASSIS_WIDTH/2,0))
        p4 = pymunk.PinJoint(front_wheel.body, chassis.body, (0,0), (0,-CHASSIS_HEIGHT/2))

        p5 = pymunk.PinJoint(dude.body, chassis.body, (0,0), (CHASSIS_WIDTH/2,0))
        p6 = pymunk.PinJoint(dude.body, chassis.body, (0,0), (0,CHASSIS_HEIGHT/2))

        self.front_motor = m1 = pymunk.constraint.SimpleMotor(front_wheel.body, chassis.body, -self.speed)
        m1.max_force = 200000
        self.back_motor = self.motor = m2 = pymunk.constraint.SimpleMotor(back_wheel.body, chassis.body, -self.speed)
        m2.max_force = 200000

        badwing.app.level.space.add(p1, p2, p3, p4, p5, p6, m1, m2)

    @classmethod
    def create(self, position=(292, 192)):
        return Skateboard(position)

    def control(self):
        return Avatar(self)

    def on_add(self, layer):
        #super().on_add(layer)
        layer.add_model(self.chassis)
        layer.add_model(self.front_wheel)
        layer.add_model(self.back_wheel)
        layer.add_model(self.dude)

    def attach_motors(self):
        if self.motors_attached:
            return
        self.front_motor.rate = self.back_motor.rate = -self.speed
        badwing.app.level.space.add(self.back_motor, self.front_motor)
        self.motors_attached = True

    def detach_motors(self):
        if not self.motors_attached:
            return
        badwing.app.level.space.remove(self.back_motor, self.front_motor)
        self.motors_attached = False

    def accelerate(self, rate=SPEED_DELTA):
        self.speed += rate
        if not self.motors_attached:
            self.attach_motors()

    def decelerate(self, rate=SPEED_DELTA):
        self.speed -= rate
        if not self.motors_attached:
            self.attach_motors()

    def coast(self):
        self.detach_motors()
        self.speed = 0
        
    @debounce(1)
    def ollie(self, impulse=(0,2000), point=(0,0)):
        self.chassis.body.apply_impulse_at_local_point(impulse, point)

    def update(self, dt):
        if self.motors_attached:
            self.front_motor.rate = self.back_motor.rate = -self.speed

class Avatar(badwing.avatar.Avatar):
    def __init__(self, skateboard):
        super().__init__()
        self.skateboard = skateboard

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.skateboard.ollie()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            '''
            if not self.left_down:
                self.skateboard.set_motor(self.skateboard.back_motor)
            '''
            self.left_down = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            '''
            if not self.right_down:
                self.skateboard.set_motor(self.skateboard.front_motor)
            '''
            self.right_down = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
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
