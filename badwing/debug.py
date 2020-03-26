
import arcade

from badwing.layer import Layer

class DebugLayer(Layer):
    def __init__(self, level, name):
        super().__init__(level, name)
        self.debug_list = arcade.ShapeElementList()

    def setup(self):
        super().setup()


    def draw(self):
        self.debug_list.draw()
        self.debug_list = arcade.ShapeElementList()
