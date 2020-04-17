import math
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull

from badwing.constants import *
import badwing.app

class Model:
    def __init__(self, sprite=None, physics=PT_STATIC, brain=None):
        self.parent = None
        self._position = (0, 0)
        self.sprite = sprite
        self.physics = physics
        self.brain = brain
        # TODO:  I hate monkey patching, but ...
        if sprite:
            sprite.model = self
        # Predicates
        self.grounded = False
        self.laddered = False
        self.jumping = False
        self.falling = False
        self.mounted = False
        self.punching = False

    def on_mount(self):
        self.mounted = True

    def on_dismount(self):
        self.mounted = False

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._position = val
        if self.sprite:
            self.sprite.position = val

    def on_add(self, layer):
        pass
        """
        if self.sprite:
            layer.add_sprite(self.sprite)
        """

    def update(self, delta_time):
        self.update_brain(delta_time)
        self.update_physics(delta_time)
        self.update_sprite(delta_time)

    def update_brain(self, delta_time):
        if self.brain:
            self.brain.update(delta_time)

    def update_physics(self, delta_time):
        pass

    def update_sprite(self, delta_time):
        pass


class Group(Model):
    id_counter = 1

    def __init__(self, physics=PT_DYNAMIC):
        super().__init__(physics=physics)
        self.id_counter += 1
        self.id = self.id_counter
        self.models = []

    def add_model(self, model):
        model.parent = self
        self.models.append(model)
        return model

    def on_add(self, layer):
        super().on_add(layer)
        for model in self.models:
            model.gid = self.id
            model.physics = self.physics
            layer.add_model(model)

class PhysicsModel(Model):
    def __init__(self, sprite=None, physics=PT_STATIC):
        super().__init__(sprite, physics)
        self.body = None
        self.shapes = []

    def on_add(self, layer):
        super().on_add(layer)
        self.create_body()
        self.create_shapes()
        badwing.app.physics_engine.space.add(self.body, self.shapes)
        self.body.model = self

    def update_sprite(self, delta_time=1/60):
        if self.sprite:
            pos = self.body.position
            self.sprite.position = pos
            self.sprite.angle = math.degrees(self.body.angle)

    def create_body(self):
        pass

    def create_shapes(self):
        self.create_hull_shapes(self.sprite, self.body, self.position)

    def create_poly_shapes(self, sprite, body, position, collision_type=PT_KINEMATIC, transform=None):
        self.shapes = []
        sprite.position = position
        center = Vec2d(position)
        points = sprite.points
        #print(points)
        polys = convex_decomposition(sprite.points, 0)
        #polys = to_convex_hull(sprite.points, .01)
        #print(polys)
        for poly in polys:
            #print(poly)
            #points = [(i.x, i.y) for i in poly ]
            points = [i - center for i in poly ]
            #print(points)
            shape = pymunk.Poly(body, points, transform)
            shape.friction = 10
            shape.elasticity = 0.2
            shape.collision_type = collision_type
            self.shapes.append(shape)

    def create_hull_shapes(self, sprite, body, position, collision_type=PT_KINEMATIC, transform=None):
        self.shapes = []
        sprite.position = position
        center = Vec2d(position)
        points = sprite.points
        #print(points)
        poly = to_convex_hull(sprite.points, .01)
        #print(poly)
        #points = [(i.x, i.y) for i in poly ]
        points = [i - center for i in poly ]
        #print(points)
        shape = pymunk.Poly(body, points, transform)
        shape.friction = 10
        shape.elasticity = 0.2
        shape.collision_type = collision_type
        self.shapes.append(shape)

class StaticModel(PhysicsModel):
    def __init__(self, sprite=None):
        super().__init__(sprite, PT_STATIC)


class DynamicModel(PhysicsModel):
    def __init__(self, sprite):
        super().__init__(sprite, PT_DYNAMIC)
    def on_add(self, layer):
        super().on_add(layer)
        for shape in self.shapes:
            shape.collision_type = PT_DYNAMIC

class KinematicModel(PhysicsModel):
    def __init__(self, sprite):
        super().__init__(sprite, PT_KINEMATIC)

    def update(self, delta_time=1/60):
        super().update(delta_time)
        if not self.laddered:
            self.body.velocity += (0, int(GRAVITY[1]*delta_time))

    def create_body(self):
        sprite = self.sprite
        position = sprite.position
        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING


        mass = DEFAULT_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        #moment = pymunk.moment_for_poly(mass, points)
        self.body = body = pymunk.Body(mass, moment, body_type=pymunk.Body.KINEMATIC)
        body.position = position
        body.model = self
        return body


class ModelFactory:
    def __init__(self, layer):
        self.layer = layer
