import math

from loguru import logger
import glm
import pymunk

from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.sprite import Sprite

from badwing.constants import *
import badwing.app
import badwing.physics as physics
import badwing.geom as geom


class Model(Node2D):
    def __init__(self, position=glm.vec2(), sprite: Sprite = None, brain=None):
        super().__init__(position, vu=sprite)
        self.layer = None
        self.brain = brain

        self.grounded = False
        self.laddered = False
        self.jumping = False
        self.falling = False
        self.mounted = False
        self.punching = False

    def _create(self):
        super()._create()
        if self.vu:
            self.layer.add_sprite(self.vu)

    def update(self, delta_time):
        self.update_brain(delta_time)
        self.update_physics(delta_time)

    def update_brain(self, delta_time):
        if self.brain:
            self.brain.update(delta_time)

    def update_physics(self, delta_time):
        pass

    def update_sprite(self, delta_time=1 / 60):
        pass
        """
        if self.sprite:
            self.sprite.position = self.position
            self.sprite.angle = self.angle
        """

    def on_mount(self, position):
        self.position = position
        self.mounted = True

    def on_dismount(self, position):
        self.position = position
        self.mounted = False


class Group(Model):
    id_counter = 1

    def __init__(self, position=glm.vec2()):
        super().__init__(position)
        self.id_counter += 1
        self.id = self.id_counter
        self.models = []

    def add_model(self, model):
        #model.parent = self
        self.models.append(model)
        return model

    def _create(self):
        super()._create()
        for model in self.models:
            model.gid = self.id
            self.layer.add_model(model)


class PhysicsModel(Model):
    def __init__(
        self,
        position=glm.vec2(),
        sprite=None,
        brain=None,
        physics=physics.StaticPhysics,
        geom=geom.HullGeom,
    ):
        super().__init__(position, sprite, brain)
        self.body = None
        self.body_offset = None
        self.shapes = []
        self._physics = physics()
        self.geom = geom()
        self.mass = DEFAULT_MASS
        self.geom_transform = self.create_geom_transform()

    @property
    def physics(self):
        return self._physics

    @physics.setter
    def physics(self, physics):
        if self._physics:
            self._physics = physics
            # badwing.app.physics_engine.space.remove(self.body, self.shapes)
            self.remove_shapes()
            self.body = self.create_body()
            self.shapes = self.create_shapes()
            # badwing.app.physics_engine.space.add(self.body, self.shapes)
            self.add_shapes()
        else:
            self._physics = physics

    def _create(self):
        super()._create()
        self.body = self.create_body()
        self.shapes = self.create_shapes()

    def _post_create(self):
        super()._post_create()
        self.add_shapes()

    def update_physics(self, delta_time=1 / 60):
        if self.body:
            self.position = self.body.position
            self.angle = math.degrees(self.body.angle)

    def create_body(self, offset=None):
        return self.physics.create_body(self, offset)

    def create_shapes(self, transform=None):
        return self.geom.create_shapes(self)

    def add_shapes(self):
        for shape in self.shapes:
            shape.collision_type = self.physics.type
            badwing.app.physics_engine.space.add(self.body, shape)

    def remove_shapes(self):
        for shape in self.shapes:
            badwing.app.physics_engine.space.remove(self.body, shape)

    def get_tx_point(self, offset):
        body_pos = self.body.position
        angle = self.body.angle
        tx = glm.mat4()
        tx = glm.rotate(tx, angle, glm.vec3(0, 0, 1))
        rel_pos = tx * glm.vec4(offset[0], offset[1], 0, 1)
        pos = rel_pos + glm.vec4(body_pos[0], body_pos[1], 0, 1)
        return (pos[0], pos[1])

    def create_geom_transform(self):
        sprite = self.vu
        if not sprite:
            return None
        #a = sprite.width / sprite.texture.width
        a = self.width / sprite.width
        #d = sprite.height / sprite.texture.height
        d = self.height / sprite.height
        t = pymunk.Transform(a=a, d=d)
        return t


class PhysicsGroup(PhysicsModel):
    id_counter = 1

    def __init__(
        self, position=glm.vec2(), physics=physics.GroupPhysics, geom=geom.GroupGeom
    ):
        super().__init__(position, physics=physics, geom=geom)
        self.id_counter += 1
        self.id = self.id_counter
        self.models = []

    def add_model(self, model):
        model.parent = self
        self.models.append(model)
        return model

    def _create(self):
        super()._create()
        for model in self.models:
            model.gid = self.id
            # model.physics = self.physics
            self.layer.add_model(model)


class StaticModel(PhysicsModel):
    def __init__(
        self,
        position=glm.vec2(),
        sprite=None,
        brain=None,
        physics=physics.StaticPhysics,
        geom=geom.HullGeom,
    ):
        super().__init__(position, sprite, brain, physics, geom)

    def update_physics(self, delta_time=1 / 60):
        pass

class DynamicModel(PhysicsModel):
    def __init__(
        self,
        position=glm.vec2(),
        sprite=None,
        brain=None,
        physics=physics.DynamicPhysics,
        geom=geom.HullGeom,
    ):
        super().__init__(position, sprite, brain, physics, geom)
        """
        print(self.physics.__class__)
        print(vars(self.physics))
        """


class KinematicModel(PhysicsModel):
    def __init__(
        self,
        position=glm.vec2(),
        sprite=None,
        brain=None,
        physics=physics.KinematicPhysics,
        geom=geom.HullGeom,
    ):
        super().__init__(position, sprite, brain, physics, geom)

    def update(self, delta_time=1 / 60):
        super().update(delta_time)
        if not self.laddered:
            self.body.velocity += (0, int(GRAVITY[1] * delta_time))

    def create_body(self):
        sprite = self.sprite
        position = sprite.position
        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        mass = DEFAULT_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        # moment = pymunk.moment_for_poly(mass, points)
        self.body = body = pymunk.Body(mass, moment, body_type=pymunk.Body.KINEMATIC)
        body.position = position
        body.model = self
        return body
