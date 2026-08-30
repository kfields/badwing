from crunge.engine.resource.sprite import SpriteAtlas

from ..character.character_brain import CharacterBrain


class RobotBrain(CharacterBrain):
    def __init__(self, atlas: SpriteAtlas):
        super().__init__(atlas)
