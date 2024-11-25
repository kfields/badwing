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
            kind = sprite.properties.get('class')
            if not kind:
                continue
            position = sprite.position
            node = kinds[kind].produce(position)
            #print(model)
            self.add_node(node)

kinds = {
    'PlayerCharacter': PlayerCharacter,
    'hero': PlayerCharacter,
    'Skateboard': Skateboard
}