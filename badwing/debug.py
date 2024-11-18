from crunge.engine import Renderer

import badwing.app
from badwing.layer import Layer


class DebugLayer(Layer):
    def __init__(self, level, name):
        super().__init__(level, name)
        badwing.app.debug_layer = self
        # self.debug_list = arcade.ShapeElementList()

    def add(self, shape):
        self.debug_list.append(shape)

    def _create(self):
        super()._create()

    def draw(self, renderer: Renderer):
        print("draw", len(self.debug_list))
        self.debug_list.draw()
        # self.debug_list = arcade.ShapeElementList()
