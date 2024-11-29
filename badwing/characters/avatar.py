import glm

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder
from badwing.character.kinematic_character import KinematicCharacter

from ..character.character_brain import CharacterBrain


class Avatar(KinematicCharacter):
    def __init__(self, position=glm.vec2(), brain=None):
        model = SpriteLoader(sprite_builder=CollidableSpriteBuilder()).load(":resources:/characters/maleAdventurer_idle.png")
        vu = SpriteVu(model)
        super().__init__(position, vu=vu, model=model, brain=brain)

    @classmethod
    def produce(self, position=glm.vec2()):
        return Avatar(position, brain=CharacterBrain())
