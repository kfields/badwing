import math

import badwing.app

class Model:
    def __init__(self, sprite):
        self.sprite = sprite

    def on_add(self, layer):
        pass

    def update(self, dt):
        pass

class PhysicsModel(Model):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.body = None

    def on_add(self, layer):
        badwing.app.level.space.add(self.body, self.shape)

class StaticModel(PhysicsModel):
    def __init__(self, sprite):
        super().__init__(sprite)

class DynamicModel(PhysicsModel):
    def __init__(self, sprite):
        super().__init__(sprite)

    def update(self, dt):
        pos = self.body.position
        self.sprite.position = pos
        self.sprite.angle = math.degrees(self.body.angle)

class Assembly(Model):
    def __init__(self):
        super().__init__(None)
        self.models = []

    def update(self, dt):
        pass