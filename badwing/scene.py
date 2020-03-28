import json
import arcade
import pymunk

from pyglet import gl

import badwing.app
from badwing.constants import *
from badwing.assets import asset
from badwing.model import Model

class Scene(arcade.application.View):
    def __init__(self, name):
        super().__init__()
        badwing.app.scene = self
        self.paused = False
        self.name = name
        self.layers = []
        self.width = 0
        self.height = 0
        self.right = 0
        self.bottom = 0
        self.left = 0
        self.top = 0
        self.dialog = None
        self.avatar_stack = []

    @property
    def avatar(self):
        return self.avatar_stack[-1]

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def add_layer(self, layer):
        self.layers.append(layer)
        return layer

    def setup(self):
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def post_setup(self):
        for layer in self.layers:
            layer.setup()

    def update(self, delta_time):
        super().update(delta_time)
        for layer in self.layers:
            layer.update(delta_time)
        if self.dialog:
            self.dialog.update(delta_time)

    def draw(self):
        self.on_draw()

    def on_draw(self):
        for layer in self.layers:
            layer.draw()
        super().on_draw()
        self.draw_dialog()

    def draw_dialog(self):
        if not self.dialog:
            return
        viewport = arcade.get_viewport()
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        self.dialog.draw()
        arcade.set_viewport(viewport[0], viewport[1], viewport[2], viewport[3])
                
    def push_avatar(self, avatar):
        self.avatar_stack.append(badwing.app.avatar)
        badwing.app.avatar = avatar

    def pop_avatar(self):
        avatar =  self.avatar_stack.pop()
        badwing.app.avatar = avatar
        return avatar

    def open_dialog(self, dialog):
        self.pause()
        self.dialog = dialog
        self.push_avatar(dialog.control())

    def close_dialog(self):
        self.dialog = None
        self.pop_avatar()
        self.resume()

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)
        badwing.app.avatar.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        super().on_key_release(key, modifiers)
        badwing.app.avatar.on_key_release(key, modifiers)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        badwing.app.avatar.on_mouse_press(x, y, button, modifiers)

