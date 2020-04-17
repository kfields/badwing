import json
import arcade
import pymunk

import badwing.app
from badwing.constants import *
import badwing.assets as assets
from badwing.model import StaticModel
from badwing.layer import Layer

class Sticker(StaticModel):
    def __init__(self, sprite):
        super().__init__(sprite)

    def create_body(self):
        sprite = self.sprite
        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        self.body = body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pymunk.Vec2d(sprite.center_x, sprite.center_y)

    def create_shapes(self):
        sprite = self.sprite
        #shape = pymunk.Poly.create_box(body, (width, height))
        vertices = []
        spriteX = sprite.center_x
        spriteY = sprite.center_y
        for point in sprite.points:
            x = point[0] - spriteX
            y = point[1] - spriteY
            vertices.append((x,y))

        shape = pymunk.Poly(self.body, vertices)
        shape.friction = 10
        #shape.collision_type = PT_STATIC
        self.shapes.append(shape)

    def update(self, dt):
        super().update(dt)
        if not DEBUG_COLLISION:
            return
        #line_strip = arcade.create_line_strip(sprite.points, (255,255,255), 1)
        line_strip = arcade.create_lines(self.sprite.points, (255,255,255), 1)
        badwing.app.scene.debug_list.append(line_strip)


class StickerLayer(Layer):
    def __init__(self, level, name):
        super().__init__(level, name)
        self.sprites = arcade.tilemap.process_layer(level.map, name, TILE_SCALING)

class PhysicsStickerLayer(StickerLayer):
    def __init__(self, level, name):
        super().__init__(level, name)

class StaticStickerLayer(PhysicsStickerLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
        for sprite in self.sprites:
            self.add_model(Sticker(sprite))

class DynamicStickerLayer(PhysicsStickerLayer):
    def __init__(self, level, name):
        super().__init__(level, name)
