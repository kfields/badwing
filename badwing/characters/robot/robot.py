from badwing.character.kinematic import KinematicCharacter
from badwing.character import CharacterSprite

class Robot(KinematicCharacter):
    def __init__(self, position=(0,0), sprite=None):
        super().__init__(position, sprite)

    @classmethod
    def produce(self, position=(0,0)):
        sprite = CharacterSprite(main_path = ":resources:/animated_characters/robot/character_robot").create()
        return Robot(position, sprite)
