import math

from loguru import logger
import glm
import pymunk

from crunge.engine.d2.entity import PhysicsEntity2D, KinematicEntity2D
from crunge.engine.d2.physics import (
    KinematicPhysics,
    DynamicPhysics,
    BoxGeom,
    BallGeom,
    HullGeom,
)

from crunge.engine.d2.sprite import SpriteVu

from badwing.constants import *
import badwing.globe
from badwing.util import debounce

from badwing.character.controller import KinematicCharacterController

PLAYER_MASS = 1


class KinematicCharacter(KinematicEntity2D):
    def __init__(self, position=glm.vec2(), vu=SpriteVu(), model=None, brain=None):
        super().__init__(position, vu=vu, model=model, brain=brain, geom=HullGeom())
        self.mass = PLAYER_MASS

    def on_mount(self, node: PhysicsEntity2D, point: glm.vec2):
        # super().on_mount(point)
        self.mounted = True
        self.position = node.get_tx_point(
            glm.vec2(point.x, point.y + self.height / 2)
        )
        logger.debug(f"mounting at {self.position}")
        self.angle = node.angle
        # print('on_mount')
        #self.physics = DynamicPhysics()
        self.physics = DynamicPhysics(glm.vec2(0, -self.height / 2))
        logger.debug(f"shapes: {self.shapes}")

    def on_dismount(self, node: PhysicsEntity2D, point: glm.vec2):
        # super().on_dismount(point)
        self.mounted = False
        self.position = node.get_tx_point(glm.vec2(point.x, point.y + self.height / 2))
        #self.position = glm.vec2(node.position[0], node.position[1] + self.height / 2)
        # self.angle = model.angle
        self.angle = 0
        self.physics = KinematicPhysics()
        badwing.globe.screen.pop_avatar()

    """
    @classmethod
    def produce(self, position=glm.vec2()):
        exit()
        #vu = CharacterVu().create()
        vu = SpriteVu()
        brain = CharacterBrain()
        return KinematicCharacter(position, vu=vu, brain=brain)
    """

    def control(self):
        return KinematicCharacterController(self)

    '''
    def create_body(self):
        if self.mounted:
            self.physics.position = glm.vec2(0, -self.height / 2)
            return self.physics.create_body(self)
        else:
            return self.physics.create_body(self)
    '''

    '''
    def create_shapes(self):
        if self.mounted:
            transform = pymunk.Transform(ty=self.height / 2)
            return self.geom.create_shapes(self, transform)
        else:
            return self.geom.create_shapes(self)
    '''
    
    """
    def update(self, delta_time=1 / 60):
        super().update(delta_time)
        #logger.debug(f"position: {self.position}")
        if not self.laddered:
            self.body.velocity += (0, int(GRAVITY[1] * delta_time))
        
        if not self.mounted:
            return
            
        pos = self.get_tx_point(glm.vec2(0, 64))
        self.position = pos
        angle = self.body.angle
        self.angle = math.degrees(angle)
    """

    """
    def update_sprite(self, delta_time=1/60):
        if not self.mounted:
            super().update_sprite(delta_time)
            return
        pos = self.get_tx_point((0, 64))
        self.sprite.position = (pos[0], pos[1])
        angle = self.body.angle
        self.sprite.angle = math.degrees(angle)
    """
