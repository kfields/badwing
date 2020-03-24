import arcade

import badwing.app

class Avatar:
    def __init__(self):
        badwing.app.avatar = self
        self.up_down = False
        self.left_down = False
        self.right_down = False
        
    def on_key_press(self, key, modifiers):
        pass

    def on_key_release(self, key, modifiers):
        pass

    def update(self, dt):
        pass