from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge.engine.d2.sprite import SpriteVuGroup
from crunge.engine.d2.scene_layer_2d import SceneLayer2D

from badwing.constants import *

if TYPE_CHECKING:
    from .level import Level


class SceneLayer(SceneLayer2D):
    def __init__(self, name: str, factory=None):
        super().__init__(name)
        self.sprites = SpriteVuGroup()
        self.factory = None
        if factory:
            self.factory = factory(self)

    @property
    def level(self) -> "Level":
        return self.scene

    def _create(self):
        super()._create()
        self.bounds = self.level.bounds
        if self.factory:
            self.factory.produce()

    def add_sprite(self, sprite):
        self.sprites.append(sprite)
        return sprite

    '''
    def update(self, delta_time):
        if badwing.globe.scene.paused:
            return
        for node in self.nodes:
            node.update(delta_time)
        self.effects.update(delta_time)
        self.sprites.update(delta_time)

    def draw(self, renderer: Renderer):
        #logger.debug(f'Layer: {self.__class__.__name__} sprites: {len(self.sprites.members)}')
        self.sprites.draw(renderer)
        #self.effects.draw(renderer)
        super().draw(renderer)
    '''