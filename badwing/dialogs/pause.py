import os
import arcade
import arcade.gui as gui

import badwing.app
import badwing.controller

from badwing.assets import asset

from badwing.scene import Scene
import badwing.dialog


class Controller(badwing.controller.Controller):
    def on_key_press(self, key, modifiers):
        pass
        #TODO: causing it to close on open :(
        '''
        if key == arcade.key.ESCAPE:
            badwing.app.scene.close_dialog()
        '''

class ResumeButton(gui.UIFlatButton):
    def __init__(self, view, center_x, center_y, width=200, height=50):
        super().__init__('Resume', center_x, center_y, width, height)
        self.view = view

    def on_press(self):
        if self.pressed:
            return
        print('resume')
        self.pressed = True
        badwing.app.scene.close_dialog()

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
        self.view.close()
        import badwing.scenes.start
        badwing.app.game.show_scene(badwing.scenes.start.StartScene)

    def on_release(self):
        self.pressed = False


class PauseDialog(badwing.dialog.Dialog):
    def __init__(self):
        super().__init__('pause')
        self.width = badwing.app.game.width
        self.height = badwing.app.game.height
        self.half_width = self.width/2
        self.half_height = self.height/2
        self.center_x = self.width / 2
        self.center_y = self.height / 2

    def control(self):
        return Controller(passthrough=self)

    def add_buttons(self):
        self.ui_manager.add_ui_element(ResumeButton(self, self.half_width, self.half_height))
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
