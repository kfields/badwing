import sys
import os

sys.path.append(os.path.abspath(__file__))

import arcade
import pymunk
import pymunk.pyglet_util

from badwing.constants import *
from badwing.player import Player
from badwing.levels.level1 import Level

draw_options = pymunk.pyglet_util.DrawOptions()

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player = Player()
        self.level = Level()

    def setup(self):
        self.level.setup()

    def on_draw(self):
        arcade.start_render()

        self.level.draw()

        self.level.space.debug_draw(draw_options)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        self.player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        self.player.on_key_release(key, modifiers)

    def on_update(self, dt):
        self.player.update(dt)
        self.level.update(dt)

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
