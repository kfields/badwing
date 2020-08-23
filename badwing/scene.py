import json
import arcade
import pymunk

from pyglet import gl

import badwing.app
from badwing.view import View
from badwing.constants import *
from badwing.debug import DebugLayer
from badwing.assets import asset
from badwing.model import Model

class Scene(View):
    def __init__(self, name):
        super().__init__()
        badwing.app.scene = self
        self.debug_layer = None
        self.ground_layer = None
        self.paused = False
        self.name = name
        self.layers = []
        self.animated_layers = []
        self.width = 0
        self.height = 0
        self.right = 0
        self.bottom = 0
        self.left = 0
        self.top = 0
        self.dialog = None
        self.controller_stack = []
        self.song = None
        self.mute = False

    @property
    def controller(self):
        return self.controller_stack[-1]

    def push_controller(self, controller):
        self.controller_stack.append(controller)
        badwing.app.controller = controller

    def pop_controller(self):
        controller =  self.controller_stack.pop()
        badwing.app.controller = controller
        return controller

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def add_layer(self, layer):
        self.layers.append(layer)
        return layer

    def add_animated_layer(self, layer):
        self.add_layer(layer)
        self.animated_layers.append(layer)
        return layer

    def pre_setup(self):
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.ui_manager.purge_ui_elements()

    def do_setup(self):
        pass
    
    def post_setup(self):
        for layer in self.layers:
            layer.setup()
        if not self.mute and self.song:
            self.song.play(volume=.5)

    def setup(self):
        self.pre_setup()
        self.do_setup()
        self.post_setup()
        if DEBUG_COLLISION:
            self.debug_layer = debug_layer = self.add_layer(DebugLayer(self, 'debug'))
            self.debug_list = debug_layer.debug_list

    def shutdown(self):
        if not self.mute and self.song:
            self.song.stop()

    def update(self, delta_time):
        super().update(delta_time)
        if self.controller:
            self.controller.update(delta_time)

        for layer in self.layers:
            layer.update(delta_time)
        for layer in self.animated_layers:
            layer.update_animation(delta_time)
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

    def open_dialog(self, dialog):
        self.dialog = dialog
        self.pause()
        dialog.open()
        self.push_controller(dialog.control())

    def close_dialog(self):
        if self.dialog:
            self.dialog.close()
        self.dialog = None
        self.pop_controller()
        self.resume()

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)
        badwing.app.controller.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        super().on_key_release(key, modifiers)
        badwing.app.controller.on_key_release(key, modifiers)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        badwing.app.controller.on_mouse_press(x, y, button, modifiers)

