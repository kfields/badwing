import math

from badwing.constants import *
import badwing.app


class Model:
    def __init__(self, sprite, brain=None):
        self.parent = None
        self.sprite = sprite
        self.physics = None
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

    def on_mount(self):
        self.mounted = True

    def on_dismount(self):
        self.mounted = False

    @property
    def position(self):
        return self.sprite.position

    @position.setter
    def position(self, val):
        self.sprite.position = val

    def on_add(self, layer):
        pass
        """
        if self.sprite:
            layer.add_sprite(self.sprite)
        """

    def update(self, delta_time):
        if self.physics:
            self.physics.update(delta_time)
        if self.brain:
            self.brain.update(delta_time)
        self.update_sprite()

    def update_sprite(self):
        pass


class Group(Model):
    def __init__(self):
        super().__init__(None)
        self.models = []

    def add_model(self, model):
        model.parent = self
        self.models.append(model)
        return model

    def on_add(self, layer):
        super().on_add(layer)
        for model in self.models:
            layer.add_model(model)

class PhysicsModel(Model):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.body = None
        self.shapes = []

    def on_add(self, layer):
        super().on_add(layer)
        badwing.app.physics_engine.space.add(self.body, self.shapes)
        self.body.model = self

    def update_sprite(self, delta_time=1/60):
        if not self.sprite:
            return
        pos = self.body.position
        self.sprite.position = pos
        self.sprite.angle = math.degrees(self.body.angle)


class StaticModel(PhysicsModel):
    def __init__(self, sprite):
        super().__init__(sprite)


class DynamicModel(PhysicsModel):
    def __init__(self, sprite):
        super().__init__(sprite)
    def on_add(self, layer):
        super().on_add(layer)
        for shape in self.shapes:
            shape.collision_type = CT_DYNAMIC

class KinematicModel(PhysicsModel):
    def __init__(self, sprite):
        super().__init__(sprite)

    """
    def update(self, delta_time):
        #self.body.position = self.sprite.position
        self.body.velocity = self.sprite.velocity  
        print(self.body.velocity)
        print(self.body.position)
        print(self.sprite.position)
    """

