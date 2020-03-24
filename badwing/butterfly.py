import json
import arcade
import pymunk

import badwing.app
from badwing.constants import *
import badwing.assets as assets
from badwing.model import Model
from badwing.tile import TileLayer

import arcade

CHARACTER_SCALING = 2

MOVEMENT_SPEED = 5
FRAMES=10
UPDATES_PER_FRAME = 7

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]

class ButterflySprite(arcade.Sprite):
    def __init__(self, main_path, orig_sprite):

        # Set up parent class
        super().__init__(center_x=orig_sprite.center_x, center_y=orig_sprite.center_y)

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = CHARACTER_SCALING

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}0.png")
        self.texture = self.idle_texture_pair[self.character_face_direction]
        # Load textures for walking
        self.walk_textures = []
        for i in range(FRAMES):
            texture = load_texture_pair(f"{main_path}{i}.png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        '''
        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
        '''
        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > (FRAMES-1) * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

class Butterfly(Model):
    def __init__(self, sprite):
        super().__init__(sprite)

    def update(self, dt):
        super().update(dt)

class ButterflyBlue(Model):
    def __init__(self, sprite):
        super().__init__(sprite)

    @classmethod
    def create(self, orig_sprite):
        sprite = ButterflySprite("assets/butterfly/01/butterfly000", orig_sprite)
        return ButterflyBlue(sprite)


class ButterflyLayer(TileLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        orig_sprites = self.sprites
        self.sprites = arcade.SpriteList()
        for orig_sprite in orig_sprites:
            print(orig_sprite.properties)
            model = ButterflyBlue.create(orig_sprite)
            self.sprites.append(model.sprite)
            self.add_model(model)
