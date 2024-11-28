import math

from loguru import logger
import glm
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull

from crunge.engine.d2.entity import KinematicEntity2D
from crunge.engine.d2.physics import KinematicPhysics, DynamicPhysics, BoxGeom, BallGeom, HullGeom
from crunge.engine.d2.sprite import Sprite, SpriteVu

from badwing.constants import *
import badwing.globe
from badwing.util import debounce

#from badwing.physics.util import check_grounding
#from badwing.character import CharacterController, CharacterVu
from badwing.character.controller import KinematicCharacterController

from .character_brain import CharacterBrain

PLAYER_MASS = 1
SLOP = 0

class KinematicCharacter(KinematicEntity2D):
    def __init__(self, position=glm.vec2(), vu=SpriteVu(), model=None, brain=None):
        super().__init__(position, vu=vu, model=model, brain=brain, geom=HullGeom)
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
        badwing.globe.scene.pop_pc()

    '''
    @classmethod
    def produce(self, position=glm.vec2()):
        exit()
        #vu = CharacterVu().create()
        vu = SpriteVu()
        brain = CharacterBrain()
        return KinematicCharacter(position, vu=vu, brain=brain)
    '''

    def control(self):
        return KinematicCharacterController(self)

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

    def update(self, delta_time=1 / 60):
        super().update(delta_time)
        #logger.debug(f"position: {self.position}")
        if not self.laddered:
            self.body.velocity += (0, int(GRAVITY[1] * delta_time))
        
        if not self.mounted:
            return
            
        pos = self.get_tx_point((0, 64))
        self.position = glm.vec2(pos[0], pos[1])
        angle = self.body.angle
        self.angle = math.degrees(angle)

    '''
    def update_sprite(self, delta_time=1/60):
        if not self.mounted:
            super().update_sprite(delta_time)
            return
        pos = self.get_tx_point((0, 64))
        self.sprite.position = (pos[0], pos[1])
        angle = self.body.angle
        self.sprite.angle = math.degrees(angle)
    '''