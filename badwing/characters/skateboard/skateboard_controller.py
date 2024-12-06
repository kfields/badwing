from crunge import sdl

from badwing.character import CharacterController

class SkateboardController(CharacterController):
    def __init__(self, skateboard):
        super().__init__(skateboard)
        self.skateboard = skateboard

    def update(self, delta_time):
        if self.up_pressed:
            self.skateboard.ollie()
        elif self.down_pressed:
            #self.skateboard.dismount()
            pass
        elif self.left_pressed:
            self.skateboard.decelerate()
        elif self.right_pressed:
            self.skateboard.accelerate()
        else:
            self.skateboard.coast()
    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        repeat = event.repeat

        match key:
            case sdl.SDLK_w:
                self.up_pressed = down
            case sdl.SDLK_s:
                self.down_pressed = down
            case sdl.SDLK_a:
                self.left_pressed = down
            case sdl.SDLK_d:
                self.right_pressed = down
    '''
    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        repeat = event.repeat

        if key == sdl.SDLK_w:
            if down:
                self.up_pressed = True
            else:
                self.up_pressed = False
        elif key == sdl.SDLK_s:
            if down:
                self.down_pressed = True
            else:
                self.down_pressed = False
        elif key == sdl.SDLK_a:
            if down:
                self.left_pressed = True
            else:
                self.left_pressed = False
        elif key == sdl.SDLK_d:
            if down:
                self.right_pressed = True
            else:
                self.right_pressed = False
    '''

    '''
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.skateboard.ollie()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.skateboard.dismount()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_down = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_down = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_down = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_down = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_down = False
    '''