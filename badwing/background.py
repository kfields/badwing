from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader
from badwing.constants import *
from badwing.tile import TileLayer

class BackgroundLayer(TileLayer):
    def __init__(self, name, filename):
        super().__init__(name)
        self.filename = filename
        self.background = None
        
    def _create(self):
        super()._create()
        #self.background = arcade.load_texture(self.filename)
        self.background = ImageTextureLoader().load(self.filename)

    '''
    def draw(self, renderer: Renderer):
        # Draw the background texture
        #(left, right, bottom, top) = viewport = self.level.window.get_viewport()
        (left, right, bottom, top) = viewport = self.level.window.viewport

        arcade.draw_lbwh_rectangle_textured(left, bottom,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        # Draw the tiles
        super().draw()
    '''