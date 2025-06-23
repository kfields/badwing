from typing import TYPE_CHECKING

from loguru import logger

from crunge import sdl

from badwing.character import CharacterController

if TYPE_CHECKING:
    from .skateboard import Skateboard


class SkateboardController(CharacterController):
    def __init__(self, skateboard: "Skateboard"):
        super().__init__(skateboard)
        self.skateboard = skateboard

    def update(self, delta_time: float):
        '''
        if self.up_pressed:
            self.skateboard.ollie()
        elif self.down_pressed:
            self.skateboard.dismount()
        '''
        if self.left_pressed:
            self.skateboard.decelerate()
        elif self.right_pressed:
            self.skateboard.accelerate()
        else:
            self.skateboard.coast()
        super().update(delta_time)

    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        repeat = event.repeat

        match key:
            case sdl.SDLK_w:
                if down and not repeat:
                    self.skateboard.ollie()
            case sdl.SDLK_s:
                if down and not repeat:
                    self.skateboard.dismount()
            case sdl.SDLK_a:
                self.left_pressed = down
            case sdl.SDLK_d:
                self.right_pressed = down
