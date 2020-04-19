import math
import glm
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull

import arcade

from badwing.constants import *
import badwing.app
from badwing.util import debounce

import badwing.physics
import badwing.geom

from badwing.model import Model, DynamicModel, KinematicModel
from badwing.physics.util import check_grounding
from badwing.character import CharacterController, CharacterSprite
from badwing.character.controller import KinematicController

PLAYER_MASS = 1
SLOP = 0
class KinematicCharacter(KinematicModel):
    def __init__(self, position=(0,0), sprite=None):
        super().__init__(position, sprite, geom=badwing.geom.HullGeom)
        self.mass = PLAYER_MASS

    def on_mount(self, model, point):
        super().on_mount(point)
        self.position = model.get_tx_point((point[0], point[1] + self.height/2 + SLOP))
        self.angle = model.angle
        #print('on_mount')
        self.physics = badwing.physics.DynamicPhysics()

    def on_dismount(self, model, point):
        super().on_dismount(point)
        #self.position = model.get_tx_point((point[0], point[1] + self.height/2 + SLOP))
        self.position = (model.position[0], model.position[1] + self.height/2)
        #self.angle = model.angle
        self.angle = 0
        self.physics = badwing.physics.KinematicPhysics()
        badwing.app.scene.pop_pc()

    @classmethod
    def create(self, position=(0,0)):
        sprite = CharacterSprite(position)
        return KinematicCharacter(position, sprite)

    def control(self):
        return KinematicController(self)

    def create_body(self):
        if self.mounted:
            offset = (0, -self.height/2 + SLOP)
            return self.physics.create_body(self, offset)
        else:
            return self.physics.create_body(self)

    def create_shapes(self):
        if self.mounted:
            transform = pymunk.Transform(ty=self.height/2 + SLOP)
            return self.geom.create_shapes(self, transform)
        else:
            return self.geom.create_shapes(self)

    # Hack in sprite transform here for now.  Move up the hierarchy later
    
    def update_sprite(self, delta_time=1/60):
        if not self.mounted:
            super().update_sprite(delta_time)
            return
        pos = self.get_tx_point((0, 64))
        self.sprite.position = (pos[0], pos[1])
        angle = self.body.angle
        self.sprite.angle = math.degrees(angle)
