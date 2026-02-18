import glm

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder
from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader

from badwing.character.dynamic_character import DynamicCharacter

from .avatar_brain import AvatarBrain


class Avatar(DynamicCharacter):
    def __init__(self, position=glm.vec2()):
        model = SpriteLoader(sprite_builder=CollidableSpriteBuilder()).load(
            ":resources:/characters/maleAdventurer_idle.png"
        )
        atlas = XmlSpriteAtlasLoader(sprite_builder=CollidableSpriteBuilder()).load(
            ":resources:/characters/male_adventurer/sheet.xml"
        )
        brain = AvatarBrain(atlas)
        super().__init__(position, vu=SpriteVu(), model=model, brain=brain)

    @classmethod
    def produce(self, position=glm.vec2()):
        return Avatar(position)
