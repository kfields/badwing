import arcade

class View(arcade.application.View):
    def __init__(self, window=None):
        super().__init__(window)
        self.ui_manager = arcade.gui.UIManager(self.window)
        self.ui_manager.enable()

    def setup(self):
        pass

    def open(self):
        self.ui_manager.enable()
        self.setup()

    def close(self):
        self.ui_manager.disable()

    def on_draw(self):
        super().on_draw()
        self.ui_manager.draw()

    def on_hide_view(self):
        super().on_hide_view()
        self.ui_manager.disable()
