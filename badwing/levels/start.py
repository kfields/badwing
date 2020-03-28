import sys
import os

import arcade

from badwing.constants import *
from badwing.assets import asset
import badwing.level

from badwing.physics.dynamic import DynamicPhysics
from badwing.physics.kinematic import KinematicPhysics
from badwing.layer import Layer
from badwing.barrier import BarrierLayer
from badwing.background import BackgroundLayer
from badwing.tile import TileLayer, StaticTileLayer
from badwing.ladder import LadderLayer

from badwing.butterfly import Butterflies

from badwing.emitter import EmitterLayer
from badwing.obstacle import ObstacleTileLayer
from badwing.debug import DebugLayer

from badwing.levels.level1 import Level as Level1

class StartButton(arcade.gui.TextButton):
    def __init__(self, view, x, y, width=110, height=50, text="Start", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.view = view

    def on_press(self):
        self.pressed = True
        level = Level1()
        level.setup()
        level.post_setup()
        badwing.app.game.show_scene(level)

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.dialoguebox.active = True

class Level(badwing.level.Level):
    def __init__(self):
        super().__init__('start')

        # Our physics engine
        #self.physics_engine = physics_engine = KinematicPhysics(k_gravity=K_GRAVITY)
        self.physics_engine = physics_engine = DynamicPhysics()
        self.space = physics_engine.space

        self.width = badwing.app.game.width
        self.height = badwing.app.game.height
        self.half_width = self.width/2
        self.half_height = self.height/2
        self.center_x = self.width / 2
        self.center_y = self.height / 2

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

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
        show_button = StartButton(self, self.half_width, self.half_height, theme=self.theme)
        self.button_list.append(show_button)

    def setup(self):
        self.theme = badwing.app.game.theme
        super().setup()

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # --- Load in a map from the tiled editor ---

        # Name of map file to load
        map_name = asset("start.tmx")
        # Name of the layer that has items for pick-up
        coins_layer_name = 'coins'

        self.add_layer(BarrierLayer(self, 'barrier'))
        self.add_layer(BackgroundLayer(self, 'background', ":resources:images/backgrounds/abstract_1.jpg"))
        self.ladder_layer = self.add_layer(LadderLayer(self, 'ladder'))
        self.ground_layer = self.add_layer(StaticTileLayer(self, 'ground'))
        self.spark_layer = self.add_layer(EmitterLayer(self, 'spark'))

        self.add_layer(BackgroundLayer(self, 'background', ":resources:images/backgrounds/abstract_1.jpg"))
        self.butterfly_layer = butterfly_layer = Layer(self, 'butterflies')
        butterflies = Butterflies.create_random(20, (0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
        self.butterfly_layer.add_model(butterflies)
        self.add_layer(butterfly_layer)

        self.obstacle_layer = self.add_layer(ObstacleTileLayer(self, 'obstacle'))
        self.object_layer = self.add_layer(ObstacleTileLayer(self, 'object'))

        #self.add_dialogue_box()
        self.add_text()
        self.add_button()

        #self.text_list.append(arcade.TextLabel("Name: ", self.center_x, self.center_y))

        if DEBUG_COLLISION:
            self.debug_layer = debug_layer = self.add_layer(DebugLayer(self, 'debug'))
            self.debug_list = debug_layer.debug_list
        

    def post_setup(self):
        super().post_setup()
        # Requires physics engine to exist first
        #self.player.control()

    def update(self, delta_time):
        super().update(delta_time)
        """ Movement and game logic """
        # Move the player with the physics engine
        self.physics_engine.update()

        self.butterfly_layer.update_animation(delta_time)


    def draw(self):
        super().draw()
        arcade.draw_text(
            "BadWing", self.center_x, self.center_y + 100, arcade.color.WHITE, 60, font_name='Verdana', align='center'
        )
