from loguru import logger

from crunge.engine import Renderer
from crunge.engine.d2.sprite import SpriteVuGroup
from crunge.engine.view_layer import ViewLayer

import badwing.app
from badwing.constants import *
from badwing.effect import EffectList

class Layer(ViewLayer):
    def __init__(self, level, name, factory=None):
        super().__init__(name)
        self.level = level
        self.width = level.width
        self.height = level.height
        self.left = level.left
        self.bottom = level.bottom
        self.right = level.right
        self.top = level.top
        self.models = []
        self.sprites = SpriteVuGroup()
        self.effects = EffectList()
        self.factory = None
        if factory:
            self.factory = factory(self)

    def _create(self):
        super()._create()
        if self.factory:
            self.factory.produce()

    def add_model(self, model):
        model.layer = self
        self.models.append(model)
        model.enable()
        return model

    def add_sprite(self, sprite):
        self.sprites.append(sprite)
        return sprite

    def add_effect(self, effect):
        self.effects.append(effect)
        return effect

    def update(self, delta_time):
        if badwing.app.scene.paused:
            return
        for model in self.models:
            model.update(delta_time)
        self.effects.update(delta_time)
        self.sprites.update(delta_time)

    def update_animation(self, delta_time):
        if badwing.app.scene.paused:
            return
        #self.sprites.update_animation(delta_time)

    def draw(self, renderer: Renderer):
        #logger.debug(f'Layer: {self.__class__.__name__} sprites: {len(self.sprites)}')
        self.sprites.draw(renderer)
        #self.effects.draw(renderer)
        super().draw(renderer)
