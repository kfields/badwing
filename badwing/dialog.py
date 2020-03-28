import arcade

class Dialog(arcade.application.View):
    def __init__(self, name):
        super().__init__()

    def setup(self):
        pass

    def draw(self):
        super().on_draw()