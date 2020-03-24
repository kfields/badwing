import math
import glm
import pymunk
from pymunk import Vec2d
import arcade

from badwing.constants import *
import badwing.app
import badwing.avatar
from badwing.model import DynamicModel, Assembly


WHEEL_RADIUS = 32
WHEEL_MASS = 1

CHASSIS_WIDTH = 128
CHASSIS_HEIGHT = 32
CHASSIS_MASS = 1

DUDE_MASS = 1

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


class Chassis(DynamicModel):
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


class Dude(DynamicModel):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)

        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        # need to offset shape for lower center of gravity

        mass = DUDE_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        self.body = body = pymunk.Body(mass, moment)

        dude_pos = Vec2d(position)
        self.body_offset = body_offset = Vec2d(0, -height/2)
        body.position = dude_pos + body_offset

        t = pymunk.Transform(ty=height/2)
        self.shape = shape = pymunk.Poly(body, sprite.points, t)
        shape.friction = 10
        shape.elasticity = 0.2

    @classmethod
    def create(self, position=(192, 192)):
        img_src = ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png"
        sprite = arcade.Sprite(img_src, CHARACTER_SCALING)
        return Dude(sprite, position)

    def on_add(self, layer):
        super().on_add(layer)
        layer.add_sprite(self.sprite)

    # Hack in sprite transform here for now.  Move up the hierarchy later
    def update(self, dt):
        body_pos = self.body.position
        angle = self.body.angle
        model = glm.mat4()
        model = glm.rotate(model, angle, glm.vec3(0, 0, 1))
        rel_pos = model * glm.vec4(0, 64, 0, 1)
        pos = rel_pos + glm.vec4(body_pos[0], body_pos[1], 0, 1) 
        self.sprite.position = (pos[0], pos[1])
        self.sprite.angle = math.degrees(angle)


class Skateboard(Assembly):
    def __init__(self, position=(292, 192)):
        super().__init__()
        self.Avatar = Avatar(self)
        self.speed = 0

        chassis_pos = Vec2d(position)
        back_wheel_pos = chassis_pos - (CHASSIS_WIDTH/2+X_PAD, Y_PAD)
        front_wheel_pos = chassis_pos - (-(CHASSIS_WIDTH/2+X_PAD), Y_PAD)
        dude_pos = chassis_pos + (0, CHASSIS_HEIGHT/2+Y_PAD*2)

        self.back_wheel = back_wheel = Wheel.create(back_wheel_pos)
        self.chassis = chassis = Chassis.create(chassis_pos)
        self.dude = dude = Dude.create(dude_pos)
        self.front_wheel = front_wheel = Wheel.create(front_wheel_pos)

        p1 = pymunk.PinJoint(back_wheel.body, chassis.body, (0,0), (-CHASSIS_WIDTH/2,0))
        p2 = pymunk.PinJoint(back_wheel.body, chassis.body, (0,0), (0,-CHASSIS_HEIGHT/2))
        p3 = pymunk.PinJoint(front_wheel.body, chassis.body, (0,0), (CHASSIS_WIDTH/2,0))
        p4 = pymunk.PinJoint(front_wheel.body, chassis.body, (0,0), (0,-CHASSIS_HEIGHT/2))

        p5 = pymunk.PinJoint(dude.body, chassis.body, (0,0), (CHASSIS_WIDTH/2,0))
        p6 = pymunk.PinJoint(dude.body, chassis.body, (0,0), (0,CHASSIS_HEIGHT/2))

        self.motor = m1 = pymunk.constraint.SimpleMotor(back_wheel.body, chassis.body, -self.speed)

        badwing.app.level.space.add(p1, p2, p3, p4, p5, p6, m1)

    @classmethod
    def create(self):
        return Skateboard()

    def on_add(self, layer):
        #super().on_add(layer)
        layer.add_model(self.chassis)
        layer.add_model(self.front_wheel)
        layer.add_model(self.back_wheel)
        layer.add_model(self.dude)

    def accelerate(self):
        self.speed += SPEED_DELTA

    def decelerate(self):
        self.speed -= SPEED_DELTA

    def update(self, dt):
        self.motor.rate = -self.speed

class Avatar(badwing.avatar.Avatar):
    def __init__(self, skateboard):
        super().__init__()
        self.skateboard = skateboard

    def update(self, dt):
        if self.left_down:
            self.skateboard.decelerate()
        elif self.right_down:
            self.skateboard.accelerate()