import arcade

from badwing.character.pc import PlayerCharacter
from badwing.character.skateboard import Skateboard, Chassis

from badwing.tile import TileLayer

class CharacterTileLayer(TileLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        orig_sprites = self.sprites
        self.sprites = arcade.SpriteList()

        for sprite in orig_sprites:
            kind = sprite.properties.get('kind')
            if not kind:
                continue
            position = sprite.position
            model = kinds[kind].create(position)
            #print(model)
            self.add_model(model)

kinds = {
    'PlayerCharacter': PlayerCharacter,
    'Skateboard': Skateboard
}