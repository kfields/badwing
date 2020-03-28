import os
import arcade

import badwing.app
import badwing.avatar

from badwing.assets import asset

from badwing.scene import Scene
import badwing.dialog

import badwing.levels.start

class Avatar(badwing.avatar.Avatar):
    def on_key_press(self, key, modifiers):
        pass
        #TODO: causing it to close on open :(
        '''
        if key == arcade.key.ESCAPE:
            badwing.app.level.close_dialog()
        '''

class NextButton(arcade.gui.TextButton):
    def __init__(self, view, x, y, width=200, height=50, text="Next", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.view = view

    def on_press(self):
        if self.pressed:
            return
        self.pressed = True
        badwing.app.game.show_scene(self.view.next_level)
        badwing.app.level.close_dialog()

    def on_release(self):
        self.pressed = False


class QuitButton(arcade.gui.TextButton):
    def __init__(self, view, x, y, width=200, height=50, text="Quit", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.view = view

    def on_press(self):
        self.pressed = True
        #print('quit')
        badwing.app.level.close_dialog()
        badwing.app.game.show_scene(badwing.levels.start.StartScreen)

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
        return Avatar(self)

    def add_buttons(self):
        #print(self.half_height)
        #print(self.half_width)
        self.button_list.append(NextButton(self, self.half_width, self.half_height, theme=self.theme))
        self.button_list.append(QuitButton(self, self.half_width, self.half_height - 100, theme=self.theme))

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
