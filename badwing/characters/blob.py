import arcade

from badwing.model import KinematicModel
from badwing.assets import asset
from badwing.effect import Effect

GROWTH_RATE = 50

class BlobSprite(arcade.Sprite):
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
    def create(self, position=(0,0)):
        sprite = BlobSprite(position)
        return Blob(position, sprite)

'''
    def draw_transformed(self,
                         left: float,
                         bottom: float,
                         width: float,
                         height: float,
                         angle: float = 0,
                         alpha: int = 255,
                         texture_transform: Matrix3x3 = Matrix3x3()):
'''
'''
class BlobSprite(Effect):
    def __init__(self, position):
        super().__init__(position)
        self.texture = arcade.load_texture(asset('stickers/blobGreen.png'))

    def draw(self):
        print('draw')
        width = self.width * 2
        height = self.height
        left = self.left - width/2
        bottom = self.bottom
        opacity = int(.25 * 255)
        angle = self.angle
        #scale = 150 / z
        #translate = scale / 500

        #matrix  = Matrix3x3().rotate(angle).scale(scale * ASPECT, scale).translate(-self.camera_x * translate, 0)
        #matrix  = arcade.Matrix3x3().shear(2, 1)
        matrix  = arcade.Matrix3x3().scale(1, 1)
        self.texture.draw_transformed(left, bottom, width, height, angle, opacity, matrix)

class Blob(Model):
    @classmethod
    def create(self, position=(0,0)):
        sprite = BlobSprite(position)
        return Blob(sprite)

    def do_setup(self):
        super().do_setup()
        #layer.add_sprite(self.sprite)
        layer.add_effect(self.sprite)
'''