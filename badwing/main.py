import sys
import os

import arcade
import pymunk

from badwing import __version__
import badwing.app
import badwing.assets
from badwing.constants import *
from badwing.player import Player
from badwing.levels.level1 import Level

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        badwing.app.game = self
        self.player = Player()
        self.level = Level()

    def setup(self):
        self.level.setup()

    def on_draw(self):
        arcade.start_render()

        self.level.draw()
        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        badwing.app.avatar.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        badwing.app.avatar.on_key_release(key, modifiers)

    def on_update(self, dt):
        badwing.app.avatar.update(dt)
        self.player.update(dt)
        self.level.update(dt)

def main(production=False):
    if not production:
        badwing.assets.assets_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../assets')
    else:
        badwing.assets.assets_dir = os.path.join(sys.prefix, 'share/badwing/assets')
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
