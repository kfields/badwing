import arcade
from arcade.gui import UIManager

class View(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)
        self.ui_manager = UIManager(self.window)
        self.ui_manager.enable()

    def setup(self):
        pass

    def open(self):
        self.ui_manager.enable()
        self.setup()

    def close(self):
        self.ui_manager.disable()

    def update(self, delta_time):
        pass

    def on_update(self, delta_time):
        super().on_update(delta_time)
        self.update(delta_time)

    def draw(self):
        self.ui_manager.draw()

    def on_draw(self):
        super().on_draw()
        self.draw()

    def on_hide_view(self):
        super().on_hide_view()
        self.ui_manager.disable()
