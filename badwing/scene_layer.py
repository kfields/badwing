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
        #self.sprites = SpriteVuGroup()
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
