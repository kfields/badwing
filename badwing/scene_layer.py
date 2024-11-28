from loguru import logger

from crunge.engine import Renderer
from crunge.engine.d2.sprite import SpriteVuGroup
from crunge.engine.d2.scene_layer_2d import SceneLayer2D

import badwing.globe
from badwing.constants import *
from badwing.effect import EffectList

class SceneLayer(SceneLayer2D):
    def __init__(self, level, name: str, factory=None):
        super().__init__(name, level.size)
        self.level = level
        #self.width = level.width
        #self.height = level.height
        self.left = level.left
        self.bottom = level.bottom
        self.right = level.right
        self.top = level.top
        #self.nodes = []
        self.sprites = SpriteVuGroup()
        self.effects = EffectList()
        self.factory = None
        if factory:
            self.factory = factory(self)

    def _create(self):
        super()._create()
        if self.factory:
            self.factory.produce()

    '''
    def add_node(self, node):
        node.layer = self
        self.nodes.append(node)
        node.enable()
        return node
    '''

    def add_sprite(self, sprite):
        exit()
        self.sprites.append(sprite)
        return sprite

    def add_effect(self, effect):
        self.effects.append(effect)
        return effect

    def update(self, delta_time):
        if badwing.globe.scene.paused:
            return
        for node in self.nodes:
            node.update(delta_time)
        self.effects.update(delta_time)
        self.sprites.update(delta_time)

    def update_animation(self, delta_time):
        if badwing.globe.scene.paused:
            return
        #self.sprites.update_animation(delta_time)

    def draw(self, renderer: Renderer):
        #logger.debug(f'Layer: {self.__class__.__name__} sprites: {len(self.sprites.members)}')
        self.sprites.draw(renderer)
        #self.effects.draw(renderer)
        super().draw(renderer)
