import os
import arcade
import arcade.gui as gui

import badwing.controller

from badwing.assets import asset

from badwing.scene import Scene
import badwing.dialog

class Controller(badwing.controller.Controller):
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            badwing.app.scene.close_dialog()

class BeatLevelDialog(badwing.dialog.Dialog):
    def __init__(self, next_level=None):
        super().__init__('beatlevel')
        self.next_level = next_level
        self.width = badwing.app.game.width
        self.height = badwing.app.game.height
        self.half_width = self.width/2
        self.half_height = self.height/2
        self.center_x = self.width / 2
        self.center_y = self.height / 2

    def control(self):
        return Controller(self)

    def add_buttons(self):
        width = 200
        height = 50
        next_button = gui.UIFlatButton(0 , 0, width, height, "Next")
        @next_button.event("on_click")
        def submit(x):
            badwing.app.scene.close_dialog()
            badwing.app.game.show_scene(self.next_level)

        quit_button = gui.UIFlatButton(0 , 0, width, height, "Quit")
        @quit_button.event("on_click")
        def submit(x):
            import badwing.app
            badwing.app.scene.close_dialog()
            import badwing.scenes.start
            badwing.app.game.show_scene(badwing.scenes.start.StartScene)

        self.ui_manager.add(
            gui.UIAnchorWidget(
                anchor_x="center_x",
                # x_align=-50,
                anchor_y="center_y",
                # y_align=-20,
                child=gui.UIBoxLayout(
                    x=0, y=0,
                    children=[ next_button.with_space_around(bottom=20), quit_button]
                )

            )
        )

    def setup(self):
        self.theme = badwing.app.game.theme
        super().setup()

        self.add_buttons()


    def update(self, delta_time):
        super().update(delta_time)

    def draw(self):
        super().draw()
        arcade.draw_text(
            "BadWing", self.center_x, self.center_y + 100, arcade.color.WHITE, 60, font_name='Verdana', align='center', width=300
        )
