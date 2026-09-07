from loguru import logger

from crunge import engine

class LevelController(engine.Controller):
    def __init__(self):
        super().__init__()
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
