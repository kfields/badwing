
import arcade
import badwing.app
from badwing.layer import Layer

class DebugLayer(Layer):
    def __init__(self, level, name):
        super().__init__(level, name)
        badwing.app.debug_layer = self
        self.debug_list = arcade.ShapeElementList()

    def add(self, shape):
        self.debug_list.append(shape)

    def setup(self):
        super().setup()

    def draw(self):
        print('draw', len(self.debug_list))
        self.debug_list.draw()
        self.debug_list = arcade.ShapeElementList()
