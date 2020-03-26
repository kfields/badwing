import math
import glm
import pymunk
from pymunk import Vec2d
import arcade

from badwing.constants import *
from badwing.util import debounce
import badwing.app
import badwing.avatar
from badwing.model import DynamicModel, Assembly
from badwing.physics.util import check_grounding

DUDE_MASS = 1

class Dude(DynamicModel):
    def __init__(self, sprite, position=(0,0)):
        super().__init__(sprite)

        width = sprite.texture.width * TILE_SCALING
        height = sprite.texture.height * TILE_SCALING

        # need to offset shape for lower center of gravity

        mass = DUDE_MASS
        moment = pymunk.moment_for_box(mass, (width, height))
        self.body = body = pymunk.Body(mass, moment)

        player_pos = Vec2d(position)
        self.body_offset = body_offset = Vec2d(0, -height/2)
        body.position = player_pos + body_offset

        t = pymunk.Transform(ty=height/2)
        shape = pymunk.Poly(body, sprite.points, t)
        shape.friction = 10
        shape.elasticity = 0.2
        self.shapes.append(shape)

    @classmethod
    def create(self, position=(192, 192)):
        img_src = ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png"
        sprite = arcade.Sprite(img_src, CHARACTER_SCALING)
        return Dude(sprite, position)

    def control(self):
        return Avatar(self)

    def on_add(self, layer):
        super().on_add(layer)
        layer.add_sprite(self.sprite)

    # Hack in sprite transform here for now.  Move up the hierarchy later
    def update(self, delta_time):
        body_pos = self.body.position
        angle = self.body.angle
        model = glm.mat4()
        model = glm.rotate(model, angle, glm.vec3(0, 0, 1))
        rel_pos = model * glm.vec4(0, 64, 0, 1)
        pos = rel_pos + glm.vec4(body_pos[0], body_pos[1], 0, 1) 
        self.sprite.position = (pos[0], pos[1])
        self.sprite.angle = math.degrees(angle)


class Avatar(badwing.avatar.Avatar):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.force = (0, 0)

    def on_key_press(self, symbol: int, modifiers: int):
        """ Handle keyboard presses. """
        if symbol == arcade.key.RIGHT:
            # Add force to the player, and set the player friction to zero
            self.force = (PLAYER_MOVE_FORCE, 0)
            self.player.shape.friction = 0
        elif symbol == arcade.key.LEFT:
            # Add force to the player, and set the player friction to zero
            self.force = (-PLAYER_MOVE_FORCE, 0)
            self.player.shape.friction = 0
        elif symbol == arcade.key.UP:
            # find out if player is standing on ground
            grounding = check_grounding(self.player)
            if grounding['body'] is not None and abs(
                    grounding['normal'].x / grounding['normal'].y) < self.player.shape.friction:
                # She is! Go ahead and jump
                self.player.body.apply_impulse_at_local_point((0, PLAYER_JUMP_IMPULSE))
        elif symbol == arcade.key.SPACE:
            self.punch()
        elif symbol == arcade.key.G:
            self.grab()

    def on_key_release(self, symbol: int, modifiers: int):
        """ Handle keyboard releases. """
        if symbol == arcade.key.RIGHT:
            # Remove force from the player, and set the player friction to a high number so she stops
            self.force = (0, 0)
            self.player.shape.friction = 15
        elif symbol == arcade.key.LEFT:
            # Remove force from the player, and set the player friction to a high number so she stops
            self.force = (0, 0)
            self.player.shape.friction = 15
        elif symbol == arcade.key.G:
            self.let_go()

    def update(self, delta_time):
        # If we have force to apply to the player (from hitting the arrow
        # keys), apply it.
        self.player.body.apply_force_at_local_point(self.force, (0, 0))

        # check_collision(self.player)

        # See if the player is standing on an item.
        # If she is, apply opposite force to the item below her.
        # So if she moves left, the box below her will have
        # a force to move to the right.
        grounding = check_grounding(self.player)
        if self.force[0] and grounding and grounding['body']:
            grounding['body'].apply_force_at_world_point((-self.force[0], 0), grounding['position'])
