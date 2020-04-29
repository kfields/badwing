import arcade

from badwing.characters import PlayerCharacter
from badwing.characters import Skateboard
from badwing.characters import Blob
from badwing.characters import Skeleton
from badwing.characters import Robot

from badwing.model import ModelFactory

class CharacterFactory(ModelFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def setup(self):
        orig_sprites = self.layer.sprites
        self.layer.sprites = arcade.SpriteList()

        for sprite in orig_sprites:
            #print(sprite)
            kind = sprite.properties.get('type')
            if not kind:
                continue
            position = sprite.position
            model = kinds[kind].create(position)
            print(model)
            self.layer.add_model(model)

kinds = {
    'PlayerCharacter': PlayerCharacter,
    'hero': PlayerCharacter,
    'Skateboard': Skateboard,
    'blob': Blob,
    'enemy': Skeleton,
    'skeleton': Skeleton,
    'Robot': Robot
}