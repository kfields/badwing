from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder

from badwing.character.kinematic_character import KinematicCharacter
from badwing.character import CharacterVu

class Robot(KinematicCharacter):
    def __init__(self, position=(0,0), vu=None):
        model = SpriteLoader(sprite_builder=CollidableSpriteBuilder()).load(":resources:/characters/robot_idle.png")
        super().__init__(position, vu=vu, model=model)

    @classmethod
    def produce(self, position=(0,0)):
        vu = CharacterVu(main_path = ":resources:/animated_characters/robot/character_robot").create()
        return Robot(position, vu)
