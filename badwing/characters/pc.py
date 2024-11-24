import glm

from badwing.character.kinematic import KinematicCharacter
from badwing.character import CharacterVu

class PlayerCharacter(KinematicCharacter):
    def __init__(self, position=glm.vec2(), vu=None):
        super().__init__(position, vu)

    @classmethod
    def produce(self, position=glm.vec2()):
        vu = CharacterVu().create()
        return PlayerCharacter(position, vu)
