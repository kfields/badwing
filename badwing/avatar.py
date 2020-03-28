import arcade

import badwing.app

class Avatar:
    def __init__(self, passthrough=None):
        #badwing.app.avatar = self
        self.passthrough = passthrough
        self.up_down = False
        self.left_down = False
        self.right_down = False
        
    def on_key_press(self, key, modifiers):
        if self.passthrough:
            self.passthrough.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        if self.passthrough:
            self.passthrough.on_key_release(key, modifiers)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.passthrough:
            self.passthrough.on_mouse_press(x, y, button, modifiers)

    def update(self, dt):
        pass