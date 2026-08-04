from crunge.engine.d2.sprite import Sprite

from badwing.model import KinematicModel
from badwing.assets import asset

GROWTH_RATE = 50

class BlobSprite(Sprite):
    def __init__(self, position):
        super().__init__(asset('stickers/blobGreen.png'), center_x=position[0], center_y=position[1])
        self.alpha = int(.5*255)
        self.grow = False
        self.min_width = self.width * .75
        self.max_width = self.width * 1.5

    def on_update(self, delta_time):
        super().on_update(delta_time)
        width = self.width
        if self.grow:                
            width += GROWTH_RATE * delta_time
            if width > self.max_width:
                self.grow = False
        else:
            width -= GROWTH_RATE * delta_time
            if width < self.min_width:
                self.grow = True
        self.width = width


class Blob(KinematicModel):
    @classmethod
    def produce(self, position=(0,0)):
        sprite = BlobSprite(position)
        return Blob(position, sprite)
