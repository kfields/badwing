import sys
import os

import arcade
import arcade.gui as gui
import pyglet

import badwing.app
from badwing.constants import *
from badwing.assets import asset
from badwing.level import Level
from badwing.controller import Controller

from badwing.physics.dynamic import DynamicPhysicsEngine
from badwing.layer import Layer
from badwing.barrier import BarrierLayer
from badwing.background import BackgroundLayer

from badwing.characters.butterfly import Butterflies


class StartScene(Level):
    def __init__(self):
        super().__init__('start')
        # Our physics engine
        self.physics_engine = physics_engine = DynamicPhysicsEngine()
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


    @classmethod
    def create(self):
        level = StartScene()
        level.setup()
        return level
        
    def get_next_level(self):
        import badwing.scenes.level1
        return badwing.scenes.level1.Level1

    def add_buttons(self):
        width = 200
        height = 50
        start_button = gui.UIFlatButton(0 , 0, width, height, "Start")
        @start_button.event("on_click")
        def submit(x):
          badwing.app.game.show_scene(self.get_next_level())

        quit_button = gui.UIFlatButton(0 , 0, width, height, "Quit")
        @quit_button.event("on_click")
        def submit(x):
          pyglet.app.exit()
        
        self.ui_manager.add(
            gui.UIAnchorLayout(
                children=[gui.UIBoxLayout(
                    children=[ start_button, quit_button],
                    space_between=20
                )]
            )
        )


    def do_setup(self):
        super().do_setup()
        self.theme = badwing.app.game.theme

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        self.add_layer(BarrierLayer(self, 'barrier'))

        self.add_layer(BackgroundLayer(self, 'background', ":resources:images/backgrounds/abstract_1.jpg"))
        self.butterfly_layer = butterfly_layer = Layer(self, 'butterflies')
        butterflies = Butterflies.create_random(20, (0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
        self.butterfly_layer.add_model(butterflies)
        self.add_animated_layer(butterfly_layer)

        self.add_buttons()        

    def post_setup(self):
        super().post_setup()
        self.push_controller(Controller())

    def update(self, delta_time):
        super().update(delta_time)
        self.physics_engine.update()

    def draw(self):
        super().draw()
        arcade.draw_text(
            "BadWing", self.center_x, self.center_y + 100, arcade.color.WHITE, 60, font_name='Verdana'
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            pyglet.app.exit()
