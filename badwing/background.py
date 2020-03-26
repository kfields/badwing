import arcade

from badwing.constants import *
from badwing.layer import Layer

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
