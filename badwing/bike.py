import pymunk
from pymunk import Vec2d
import arcade

from badwing.constants import *
import badwing.app
from badwing.model import Model, Assembly


WHEEL_RADIUS = 32
WHEEL_MASS = 1
CHASSIS_WIDTH = 128
CHASSIS_HEIGHT = 32
CHASSIS_MASS = 1
X_PAD = 32
Y_PAD = 32

class Wheel(Model):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)
        mass = WHEEL_MASS
        radius = WHEEL_RADIUS
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self.body = body = pymunk.Body(mass, inertia)
        body.position = position

        self.shape = shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9


    @classmethod
    def create(self, position=(0,0)):
        img_src = "assets/items/coinGold.png"
        sprite = arcade.Sprite(img_src, CHARACTER_SCALING)
        return Wheel(sprite, position)

    def on_add(self, layer):
        super().on_add(layer)
        layer.add_sprite(self.sprite)


class Chassis(Model):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)

        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        mass = CHASSIS_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        self.body = body = pymunk.Body(mass, moment)
        body.position = position

        self.shape = shape = pymunk.Poly.create_box(body, (width, height))
        shape.friction = 10
        shape.elasticity = 0.2

    @classmethod
    def create(self, position=(192, 192)):
        img_src = "assets/map/boxCrate.png"
        sprite = arcade.Sprite(img_src, CHARACTER_SCALING, image_width=CHASSIS_WIDTH, image_height=CHASSIS_HEIGHT)
        return Chassis(sprite, position)

    def on_add(self, layer):
        super().on_add(layer)
        layer.add_sprite(self.sprite)



class Bike(Assembly):
    def __init__(self, position=(292, 192)):
        self.chWd = CHASSIS_WIDTH
        self.chHt = CHASSIS_HEIGHT
        chassisXY = Vec2d(position)
        back_wheel_position = chassisXY - (self.chWd/2+X_PAD, Y_PAD)
        front_wheel_position = chassisXY - (-(self.chWd/2+X_PAD), Y_PAD)

        self.back_wheel = back_wheel = Wheel.create(back_wheel_position)
        self.chassis = chassis = Chassis.create(chassisXY)
        self.front_wheel = front_wheel = Wheel.create(front_wheel_position)
        '''
        m1 = pymunk.constraint.SimpleMotor(back_wheel.body, chassis.body, -1)
        #j1 = pymunk.constraint.PinJoint(back_wheel.body, chassis.body, anchor_a=(0,0), anchor_b=(-64, 0))
        j1 = pymunk.constraint.DampedSpring(back_wheel.body, chassis.body, anchor_a=(0,0), anchor_b=(-64, 0), rest_length=128, stiffness=100, damping=1)
        #m2 = pymunk.constraint.SimpleMotor(front_wheel.body, chassis.body, -1)
        j2 = pymunk.constraint.DampedSpring(front_wheel.body, chassis.body, anchor_a=(0,0), anchor_b=(64, 0), rest_length=128, stiffness=100, damping=1)
        #j2 = pymunk.constraint.PinJoint(front_wheel.body, chassis.body, anchor_a=(0,0), anchor_b=(64, 0))
        '''
        p1 = pymunk.PinJoint(back_wheel.body, chassis.body, (0,0), (-self.chWd/2,0))
        p2 = pymunk.PinJoint(front_wheel.body, chassis.body, (0,0), (self.chWd/2,0))
        p3 = pymunk.PinJoint(back_wheel.body, chassis.body, (0,0), (0,-self.chHt/2))
        p4 = pymunk.PinJoint(front_wheel.body, chassis.body, (0,0), (0,-self.chHt/2))

        m1 = pymunk.constraint.SimpleMotor(back_wheel.body, chassis.body, -1)

        badwing.app.level.space.add(p1, p2, p3, p4, m1)

    @classmethod
    def create(self):
        return Bike()

    def on_add(self, layer):
        #super().on_add(layer)
        layer.add_model(self.chassis)
        layer.add_model(self.front_wheel)
        layer.add_model(self.back_wheel)
