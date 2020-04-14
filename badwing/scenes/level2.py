import sys
import os

import arcade

import badwing.app
from badwing.constants import *
from badwing.assets import asset
from badwing.scenes.level1 import Level1


class Level2(Level1):
    @classmethod
    def create(self):
        level = Level2()
        level.setup()
        level.post_setup()
        return level

    #next level
    def get_next_level(self):
        import badwing.scenes.end
        return badwing.scenes.end.EndScreen
