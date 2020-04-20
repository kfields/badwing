import arcade

from badwing.model import KinematicModel
from badwing.assets import asset

class EnemySprite(arcade.Sprite):
    def __init__(self, position):
        super().__init__(asset('stickers/skeleton.png'), center_x=position[0], center_y=position[1])

class Enemy(KinematicModel):
    @classmethod
    def create(self, position=(0,0)):
        sprite = EnemySprite(position)
        return Enemy(position, sprite)
