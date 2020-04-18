import math
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull

from badwing.constants import *
import badwing.app
import badwing.physics as physics
import badwing.geom as geom

class Model:
    def __init__(self, position=(0,0), sprite=None, brain=None):
        self.layer = None
        self.parent = None
        self.position = position
        self.width = 0
        self.height = 0
        self.angle = 0
        self.transform = None # Body offset from model
        self.sprite = sprite
        self.radius = 0
        if sprite:
            self.width = sprite.texture.width * TILE_SCALING
            self.height = sprite.texture.height * TILE_SCALING
            self.radius = self.width / 2
            
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

    def setup(self, layer):
        self.layer = layer
        self.pre_setup()
        self.do_setup()
        self.post_setup()

    def pre_setup(self):
        pass

    def do_setup(self):
        pass

    def post_setup(self):
        pass

    '''
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._position = val
        if self.sprite:
            self.sprite.position = val
    '''
    def do_setup(self):
        if self.sprite and len(self.sprite.sprite_lists) == 0:
            self.layer.add_sprite(self.sprite)

    def update(self, delta_time):
        self.update_brain(delta_time)
        self.update_physics(delta_time)
        self.update_sprite(delta_time)

    def update_brain(self, delta_time):
        if self.brain:
            self.brain.update(delta_time)

    def update_physics(self, delta_time):
        pass

    def update_sprite(self, delta_time=1/60):
        if self.sprite:
            self.sprite.position = self.position
            self.sprite.angle = self.angle

    def on_mount(self):
        self.mounted = True

    def on_dismount(self):
        self.mounted = False

class Group(Model):
    id_counter = 1

    def __init__(self, position=(0,0)):
        super().__init__(position)
        self.id_counter += 1
        self.id = self.id_counter
        self.models = []

    def add_model(self, model):
        model.parent = self
        self.models.append(model)
        return model

    def do_setup(self):
        super().do_setup()
        for model in self.models:
            model.gid = self.id
            self.layer.add_model(model)

class PhysicsModel(Model):
    def __init__(self, position=(0,0), sprite=None, brain=None, physics=physics.StaticPhysics, geom=geom.HullGeom):
        super().__init__(position, sprite, brain)
        self.body = None
        self.shapes = []
        self.physics = physics()
        self.geom = geom()
        self.mass = DEFAULT_MASS

    def do_setup(self):
        super().do_setup()
        self.create_body()
        self.create_shapes()

    def post_setup(self):
        for shape in self.shapes:
            shape.collision_type = self.physics.type

        badwing.app.physics_engine.space.add(self.body, self.shapes)
        self.body.model = self

    def update_physics(self, delta_time=1/60):
        if self.body:
            self.position = self.body.position
            self.angle = math.degrees(self.body.angle)

    def create_body(self):
        self.body = self.physics.create_body(self)

    def create_shapes(self):
        self.shapes = self.geom.create_shapes(self)

class PhysicsGroup(PhysicsModel):
    id_counter = 1

    def __init__(self, position=(0,0), physics=physics.DynamicPhysics, geom=geom.GroupGeom):
        super().__init__(position, physics=physics, geom=geom)
        self.id_counter += 1
        self.id = self.id_counter
        self.models = []

    def add_model(self, model):
        model.parent = self
        self.models.append(model)
        return model

    def do_setup(self):
        super().do_setup()
        for model in self.models:
            model.gid = self.id
            model.physics = self.physics
            self.layer.add_model(model)

    def post_setup(self):
        pass

class StaticModel(PhysicsModel):
    def __init__(self, position=(0,0), sprite=None, brain=None, physics=physics.StaticPhysics, geom=geom.HullGeom):
        super().__init__(position, sprite, brain, physics, geom)


class DynamicModel(PhysicsModel):
    def __init__(self, position=(0,0), sprite=None, brain=None, physics=physics.DynamicPhysics, geom=geom.HullGeom):
        super().__init__(position, sprite, brain, physics, geom)
        '''
        print(self.physics.__class__)
        print(vars(self.physics))
        '''

class KinematicModel(PhysicsModel):
    def __init__(self, position=(0,0), sprite=None, brain=None, physics=physics.KinematicPhysics, geom=geom.HullGeom):
        super().__init__(position, sprite, brain, physics, geom)

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
