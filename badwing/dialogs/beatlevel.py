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
        

class NextButton(gui.UIFlatButton):
    def __init__(self, view, center_x, center_y, width=200, height=50):
        super().__init__('Next', center_x, center_y, width, height)
        self.view = view

    def on_press(self):
        if self.pressed:
            return
        self.pressed = True
        badwing.app.scene.close_dialog()
        badwing.app.game.show_scene(self.view.next_level)

    def on_release(self):
        self.pressed = False


class QuitButton(gui.UIFlatButton):
    def __init__(self, view, center_x, center_y, width=200, height=50):
        super().__init__('Quit', center_x, center_y, width, height)
        self.view = view

    def on_press(self):
        if self.pressed:
            return
        self.pressed = True
        #print('quit')
        import badwing.app
        badwing.app.scene.close_dialog()
        import badwing.scenes.start
        badwing.app.game.show_scene(badwing.scenes.start.StartScene)

    def on_release(self):
        self.pressed = False


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
        #print(self.half_height)
        #print(self.half_width)
        self.ui_manager.add_ui_element(NextButton(self, self.half_width, self.half_height))
        self.ui_manager.add_ui_element(QuitButton(self, self.half_width, self.half_height - 100))

    def setup(self):
        self.theme = badwing.app.game.theme
        super().setup()

        self.add_buttons()


    def update(self, delta_time):
        super().update(delta_time)

    def draw(self):
        super().draw()
        arcade.draw_text(
            "BadWing", self.center_x, self.center_y + 100, arcade.color.WHITE, 60, font_name='Verdana', align='center'
        )
