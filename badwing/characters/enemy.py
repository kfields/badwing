import arcade

from badwing.model import Model
from badwing.assets import asset

class EnemySprite(arcade.Sprite):
    def __init__(self, position):
        super().__init__(center_x=position[0], center_y=position[1])
        self.texture = arcade.load_texture(asset('stickers/skeleton.png'))

class Enemy(Model):
    @classmethod
    def create(self, position=(0,0)):
        sprite = EnemySprite(position)
        return Enemy(position, sprite)

    def on_add(self, layer):
        super().on_add(layer)
        layer.add_sprite(self.sprite)
