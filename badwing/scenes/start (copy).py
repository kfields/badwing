import os
import arcade

import badwing.app
from badwing.scene import Scene
from badwing.assets import asset

class ShowButton(arcade.gui.TextButton):
    def __init__(self, dialoguebox, x, y, width=110, height=50, text="Show", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.dialoguebox = dialoguebox

    def on_press(self):
        if not self.dialoguebox.active:
            self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.dialoguebox.active = True


class CloseButton(arcade.gui.TextButton):
    def __init__(self, dialoguebox, x, y, width=110, height=50, text="Close", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.dialoguebox = dialoguebox

    def on_press(self):
        if self.dialoguebox.active:
            self.pressed = True

    def on_release(self):
        if self.pressed and self.dialoguebox.active:
            self.pressed = False
            self.dialoguebox.active = False


class StartScene(Scene):
    def __init__(self):
        super().__init__('start')
        self.width = badwing.app.game.width
        self.height = badwing.app.game.height
        self.half_width = self.width/2
        self.half_height = self.height/2

    def add_dialogue_box(self):
        #color = (220, 228, 255)
        color = (0, 0, 0)
        dialoguebox = arcade.gui.DialogueBox(self.half_width, self.half_height, self.half_width*1.1,
                                             self.half_height*1.5, color, self.theme)
        close_button = CloseButton(dialoguebox, self.half_width, self.half_height-(self.half_height/2) + 40,
                                   theme=self.theme)
        dialoguebox.button_list.append(close_button)
        message = "Hello I am a Dialogue Box."
        dialoguebox.text_list.append(arcade.gui.TextBox(message, self.half_width, self.half_height, self.theme.font_color))
        self.dialogue_box_list.append(dialoguebox)

    def add_text(self):
        message = "Press this button to activate the Dialogue Box"
        self.text_list.append(arcade.gui.TextBox(message, self.half_width-50, self.half_height))

    def add_button(self):
        show_button = ShowButton(self.dialogue_box_list[0], self.width-100, self.half_height, theme=self.theme)
        self.button_list.append(show_button)

    def setup(self):
        self.theme = badwing.app.game.theme
        super().setup()
        print('setup')
        self.add_dialogue_box()
        self.add_text()
        self.add_button()

    def update(self, delta_time):
        super().update(delta_time)
        if self.dialogue_box_list[0].active:
            return
