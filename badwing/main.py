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

    def on_update(self, delta_time):
        badwing.app.avatar.update(delta_time)
        self.player.update(delta_time)
        self.level.update(delta_time)

def main(production=False):
    pip_assets_dir = os.path.join(sys.prefix, 'share/badwing/assets')
    is_pip_install = os.path.isdir(pip_assets_dir)
    if is_pip_install:
        badwing.assets.assets_dir = pip_assets_dir
    else:
        badwing.assets.assets_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../assets')
    
    if not production:
        if is_pip_install:
            raise Exception('You need to run this in the project root directory!')
    else:
        pass
    
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
