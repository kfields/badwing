import json
import arcade
import pymunk

import badwing.app
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
        if badwing.app.scene.paused:
            return
        for model in self.models:
            model.update(dt)

    def update_animation(self, delta_time):
        if badwing.app.scene.paused:
            return
        self.sprites.update_animation(delta_time)

    def draw(self):
        self.sprites.draw()
