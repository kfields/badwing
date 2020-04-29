from badwing.character.kinematic import KinematicCharacter
from badwing.character import CharacterSprite

class Robot(KinematicCharacter):
    def __init__(self, position=(0,0), sprite=None):
        super().__init__(position, sprite)

    @classmethod
    def create(self, position=(0,0)):
        sprite = CharacterSprite(position, main_path = ":resources:images/animated_characters/robot/robot")
        return Robot(position, sprite)
