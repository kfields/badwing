import json
import arcade
import pymunk

from badwing.constants import *
from badwing.model import Model

class Layer:
    def __init__(self, level, name):
        self.level = level
        self.name = name
        self.models = []
        self.sprites = arcade.SpriteList()

    def setup(self):
        pass

    def add_sprite(self, sprite):
        self.sprites.append(sprite)
        return sprite

    def add_model(self, model):
        self.models.append(model)
        model.on_add(self)
        return model

    def update(self, dt):
        for model in self.models:
            model.update(dt)

    def update_animation(self, delta_time):
        self.sprites.update_animation(delta_time)

    def draw(self):
        self.sprites.draw()

class BackgroundLayer(Layer):
    def __init__(self, level, name, filename):
        super().__init__(level, name)
        self.filename = filename
        self.background = None
    def setup(self):
        super().setup()
        self.background = arcade.load_texture(self.filename)
    def draw(self):
        # Draw the background texture
        (left, right, bottom, top) = viewport = arcade.get_viewport()
        arcade.draw_lrwh_rectangle_textured(left, bottom,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
