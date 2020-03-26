import math
import random
import arcade
import pymunk

import badwing.app
from badwing.constants import *
from badwing.util import debounce
import badwing.assets as assets
from badwing.model import Model
from badwing.tile import TileLayer

from badwing.butterfly.brain import ButterflyBrain

CHARACTER_SCALING = .5

MOVEMENT_SPEED = 5
FRAMES = 9
UPDATES_PER_FRAME = 2

# Constants used to track if the player is facing left or right
RIGHT_FACING = 1
LEFT_FACING = 0

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

        # --- Load Textures ---

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}0.png")
        self.texture = self.idle_texture_pair[self.character_face_direction]
        # Load textures for walking
        self.walk_textures = []
        for i in range(FRAMES):
            texture = load_texture_pair(f"{main_path}{i}.png")
            self.walk_textures.append(texture)

    @debounce(1)
    def face_left(self):
        self.character_face_direction = LEFT_FACING

    @debounce(1)
    def face_right(self):
        self.character_face_direction = RIGHT_FACING

    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.face_left()
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.face_right()
        
        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
        
        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > (FRAMES-1) * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

class Butterfly(Model):
    def __init__(self, sprite):
        super().__init__(sprite, ButterflyBrain(self))

    @classmethod
    def create(self, orig_sprite):
        kind = orig_sprite.properties['kind']
        model = kinds[kind].create(orig_sprite)
        return model

class ButterflyAqua(Butterfly):
    def __init__(self, sprite):
        super().__init__(sprite)

    @classmethod
    def create(self, orig_sprite):
        sprite = ButterflySprite("assets/butterfly/aqua/G9Butterfly000", orig_sprite)
        return ButterflyBlue(sprite)

class ButterflyBlue(Butterfly):
    def __init__(self, sprite):
        super().__init__(sprite)

    @classmethod
    def create(self, orig_sprite):
        sprite = ButterflySprite("assets/butterfly/blue/butterfly000", orig_sprite)
        return ButterflyBlue(sprite)

class ButterflyBrown(Butterfly):
    def __init__(self, sprite):
        super().__init__(sprite)

    @classmethod
    def create(self, orig_sprite):
        sprite = ButterflySprite("assets/butterfly/brown/G5Butterfly000", orig_sprite)
        return ButterflyBrown(sprite)

class ButterflyCyan(Butterfly):
    def __init__(self, sprite):
        super().__init__(sprite)

    @classmethod
    def create(self, orig_sprite):
        sprite = ButterflySprite("assets/butterfly/cyan/G6Butterfly000", orig_sprite)
        return ButterflyCyan(sprite)

class ButterflyGreen(Butterfly):
    def __init__(self, sprite):
        super().__init__(sprite)

    @classmethod
    def create(self, orig_sprite):
        sprite = ButterflySprite("assets/butterfly/green/G2Butterfly000", orig_sprite)
        return ButterflyGreen(sprite)

class ButterflyIridescent(Butterfly):
    def __init__(self, sprite):
        super().__init__(sprite)

    @classmethod
    def create(self, orig_sprite):
        sprite = ButterflySprite("assets/butterfly/iridescent/G7Butterfly000", orig_sprite)
        return ButterflyIridescent(sprite)

class ButterflyRed(Butterfly):
    def __init__(self, sprite):
        super().__init__(sprite)

    @classmethod
    def create(self, orig_sprite):
        sprite = ButterflySprite("assets/butterfly/red/G8Butterfly000", orig_sprite)
        return ButterflyRed(sprite)

class ButterflyTan(Butterfly):
    def __init__(self, sprite):
        super().__init__(sprite)

    @classmethod
    def create(self, orig_sprite):
        sprite = ButterflySprite("assets/butterfly/tan/G4Butterfly000", orig_sprite)
        return ButterflyTan(sprite)

class ButterflyTeal(Butterfly):
    def __init__(self, sprite):
        super().__init__(sprite)

    @classmethod
    def create(self, orig_sprite):
        sprite = ButterflySprite("assets/butterfly/teal/G3Butterfly000", orig_sprite)
        return ButterflyTeal(sprite)


kinds = {
    'ButterflyBlue': ButterflyBlue,
    'ButterflyAqua': ButterflyAqua,
    'ButterflyBrown': ButterflyBrown,
    'ButterflyCyan': ButterflyCyan,
    'ButterflyGreen': ButterflyGreen,
    'ButterflyIridescent': ButterflyIridescent,
    'ButterflyRed': ButterflyRed,
    'ButterflyTan': ButterflyTan,
    'ButterflyTeal': ButterflyTeal
}

class ButterflyLayer(TileLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        orig_sprites = self.sprites
        self.sprites = arcade.SpriteList()
        for orig_sprite in orig_sprites:
            #print(vars(orig_sprite))
            #print(orig_sprite.properties)
            model = Butterfly.create(orig_sprite)
            self.sprites.append(model.sprite)
            self.add_model(model)

