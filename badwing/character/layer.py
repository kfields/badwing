import arcade

from badwing.characters import PlayerCharacter
from badwing.characters import Skateboard

from badwing.tile import TileLayer

class CharacterTileLayer(TileLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        orig_sprites = self.sprites
        self.sprites = arcade.SpriteList()

        for sprite in orig_sprites:
            kind = sprite.properties.get('type')
            if not kind:
                continue
            position = sprite.position
            model = kinds[kind].create(position)
            #print(model)
            self.add_model(model)

kinds = {
    'PlayerCharacter': PlayerCharacter,
    'hero': PlayerCharacter,
    'Skateboard': Skateboard
}