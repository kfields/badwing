import json
import pymunk

from crunge.engine.d2.scene_2d import Scene2D
import badwing.globe
from badwing.constants import *
from badwing.debug import DebugLayer
from badwing.assets import asset


class Scene(Scene2D):
    def __init__(self, name):
        super().__init__()
        badwing.globe.scene = self
        self.debug_layer = None
        self.ground_layer = None
        self.paused = False
        self.name = name
        self.animated_layers = []
        self.right = 0
        self.bottom = 0
        self.left = 0
        self.top = 0
        self.dialog = None
        self.controller_stack = []
        self.song = None
        self.mute = False
        self.songPlayer = None

    @property
    def controller(self):
        if not self.controller_stack:
            return None
        if len(self.controller_stack) == 0:
            return None
        return self.controller_stack[-1]

    def push_controller(self, controller):
        self.controller_stack.append(controller)
        badwing.globe.controller = controller

    def pop_controller(self):
        controller = self.controller_stack.pop()
        badwing.globe.controller = controller
        return controller

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def add_animated_layer(self, layer):
        self.add_layer(layer)
        self.animated_layers.append(layer)
        return layer

    """
    def pre_setup(self):
        #arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        pass
        #arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def do_setup(self):
        pass
    
    def post_setup(self):
        for layer in self.layers:
            layer.create()
        if not self.mute and self.song:
            self.songPlayer = self.song.play(volume=.5)
    """

    def _create(self):
        super()._create()
        if DEBUG_COLLISION:
            self.debug_layer = debug_layer = self.add_layer(DebugLayer(self, "debug"))
            self.debug_list = debug_layer.debug_list

    def _post_create(self):
        super()._post_create()
        for layer in self.layers:
            layer.create()
        """
        if not self.mute and self.song:
            self.songPlayer = self.song.play(volume=.5)
        """

    def shutdown(self):
        if not self.mute and self.song:
            self.song.stop(self.songPlayer)

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

    """
    def draw(self):
        for layer in self.layers:
            layer.draw()
        super().draw()
        self.draw_dialog()
    """

    def draw_dialog(self):
        if not self.dialog:
            return
        viewport = self.window.get_viewport()
        self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        self.dialog.draw()
        self.window.set_viewport(viewport[0], viewport[1], viewport[2], viewport[3])

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
        badwing.globe.controller.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        super().on_key_release(key, modifiers)
        badwing.globe.controller.on_key_release(key, modifiers)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        badwing.globe.controller.on_mouse_press(x, y, button, modifiers)
