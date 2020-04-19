from badwing.character.kinematic import KinematicCharacter
from badwing.character import CharacterSprite

class PlayerCharacter(KinematicCharacter):
    def __init__(self, position=(0,0), sprite=None):
        super().__init__(position, sprite)

    @classmethod
    def create(self, position=(0,0)):
        sprite = CharacterSprite(position)
        return PlayerCharacter(position, sprite)
