import math

import badwing.app


class Model:
    @property
    def position(self):
        return self.sprite.position

    @position.setter
    def position(self, val):
        self.sprite.position = val

    def __init__(self, sprite, brain=None):
        self.sprite = sprite
        self.brain = brain

    def on_add(self, layer):
        pass
        '''
        if self.sprite:
            layer.add_sprite(self.sprite)
        '''
    def update(self, delta_time):
        if self.brain:
            self.brain.update(delta_time)


class Group(Model):
    def __init__(self):
        super().__init__(None)
        self.models = []

    def add_model(self, model):
        self.models.append(model)
    
    def on_add(self, layer):
        super().on_add(layer)
        for model in self.models:
            layer.add_model(model)

    def update(self, dt):
        pass


class PhysicsModel(Model):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.body = None
        self.shapes = []

    def on_add(self, layer):
        super().on_add(layer)
        badwing.app.level.space.add(self.body, self.shapes)


class StaticModel(PhysicsModel):
    def __init__(self, sprite):
        super().__init__(sprite)


class DynamicModel(PhysicsModel):
    def __init__(self, sprite):
        super().__init__(sprite)

    def update(self, delta_time):
        pos = self.body.position
        self.sprite.position = pos
        self.sprite.angle = math.degrees(self.body.angle)


class KinematicModel(PhysicsModel):
    def __init__(self, sprite):
        super().__init__(sprite)

    def update(self, delta_time):
        self.body.position = self.sprite.position
