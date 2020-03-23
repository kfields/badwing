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

    def add_sprite(self, sprite):
        print(sprite)
        self.sprites.append(sprite)
        return sprite

    def add_model(self, model):
        self.models.append(model)
        model.on_add(self)
        return model

    def update(self, dt):
        for model in self.models:
            model.update(dt)

    def draw(self):
        self.sprites.draw()
