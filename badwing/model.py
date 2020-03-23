import math

import badwing.app

class Model:
    def __init__(self, sprite):
        self.sprite = sprite
        self.body = None

    def on_add(self, layer):
        badwing.app.level.space.add(self.body, self.shape)

    def update(self, dt):
        pos = self.body.position
        #print(pos)
        # self.sprite.position = pos
        self.sprite.center_x = pos.x
        self.sprite.center_y = pos.y
        self.sprite.angle = math.degrees(self.body.angle)

class Assembly(Model):
    def __init__(self):
        super().__init__(None)
        self.models = []

    def update(self, dt):
        pass