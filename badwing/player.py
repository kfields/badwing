import arcade

import badwing.app

class Player:
    def __init__(self):
        badwing.app.player = self
        self.left_down = False
        self.right_down = False
        
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            pass
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_down = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_down = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_down = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_down = False

    def update(self, dt):
        if self.left_down:
            badwing.app.skateboard.decelerate()
        elif self.right_down:
            badwing.app.skateboard.accelerate()