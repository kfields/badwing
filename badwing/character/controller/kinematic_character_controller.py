from loguru import logger
import glm

from crunge import sdl
import crunge.engine.d2.physics.globe as physics_globe
from crunge.engine.d2.node_2d import Node2D
import badwing.globe
from badwing.constants import *

from badwing.character.controller import CharacterController

class KinematicCharacterController(CharacterController):
    def __init__(self, avatar: Node2D):
        super().__init__(avatar)
        self.physics_engine = physics_globe.physics_engine
        self.avatar = avatar
        self.force = glm.vec2()
        #self.jump_sound = arcade.load_sound(":resources:/sounds/jump1.wav")
        #
        self.character_layer = badwing.globe.scene.character_layer
        self.platforms = badwing.globe.scene.ground_layer.nodes
        self.ladder_layer = badwing.globe.scene.ladder_layer

        self.jumps_since_ground = 0
        self.allowed_jumps = 1
        self.allow_multi_jump = False

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

    def mount(self):
        #hit_list = arcade.check_for_collision_with_list(self.pc_sprite, self.character_layer.sprites)
        hit_list = self.character_layer.query_intersection(self.avatar.bounds)
        for node in hit_list:
            if isinstance(node, badwing.characters.Chassis):
                mount = node.group
                mount.mount(self.avatar)
                badwing.globe.scene.push_avatar(mount)

    def is_on_ladder(self):
        laddered = self.node.laddered
        if self.ladder_layer:
            #hit_list = check_for_collision_with_list(self.pc_sprite, self.ladders)
            hit_list = self.ladder_layer.query_intersection(self.avatar.bounds)
            if len(hit_list) > 0:
                #logger.debug(f"on ladder: {hit_list}")
                logger.debug(f"avatar bounds: {self.avatar.bounds}")
                for node in hit_list:
                    logger.debug(f"bounds: {node.bounds}")

                self.node.laddered = laddered = True
            else:
                self.node.laddered = laddered = False
        return laddered

    def can_jump(self, y_distance=5) -> bool:
        # Move down to see if we are on a platform
        self.pc_sprite.center_y -= y_distance

        # Check for wall hit
        hit_list = check_for_collision_with_list(self.pc_sprite, self.platforms)

        self.pc_sprite.center_y += y_distance

        if len(hit_list) > 0:
            self.jumps_since_ground = 0

        if len(hit_list) > 0 or self.allow_multi_jump and self.jumps_since_ground < self.allowed_jumps:
            return True
        else:
            return False

    def enable_multi_jump(self, allowed_jumps: int):
        self.allowed_jumps = allowed_jumps
        self.allow_multi_jump = True

    def disable_multi_jump(self):
        self.allow_multi_jump = False
        self.allowed_jumps = 1
        self.jumps_since_ground = 0

    def jump(self, velocity: int):
        self.pc_sprite.change_y = velocity
        self.increment_jump_counter()

    def increment_jump_counter(self):
        if self.allow_multi_jump:
            self.jumps_since_ground += 1

    def process_keychange(self):
        delta_x, delta_y = 0, 0
        if self.avatar.grounded:
            self.avatar.jumping = False
            self.jump_needs_reset = False

        '''
        if self.avatar.grounded or self.avatar.falling:
            self.avatar.jumping = False
        '''

        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.is_on_ladder():
                delta_y = PLAYER_MOVEMENT_SPEED
            #if not self.avatar.jumping:
            if not self.avatar.jumping and not self.jump_needs_reset:
            #if self.avatar.grounded:
                logger.debug("Jumping")
                self.avatar.jumping = True
                self.jump_needs_reset = True
                delta_y = PLAYER_JUMP_SPEED
                #arcade.play_sound(self.jump_sound)
        if self.down_pressed and not self.up_pressed:
            if self.is_on_ladder():
                delta_y = -PLAYER_MOVEMENT_SPEED
            else:
                self.mount()

        # Process up/down when on a ladder and no movement
        if self.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                delta_y = 0
            elif self.up_pressed and self.down_pressed:
                delta_y = 0

        # Process left/right
        self.avatar.falling = not self.avatar.grounded and not self.avatar.laddered and not self.avatar.jumping
        #self.avatar.falling = not self.avatar.grounded and not self.avatar.laddered

        if self.right_pressed and not self.left_pressed:
        #if (self.avatar.grounded or self.avatar.laddered) and self.right_pressed and not self.left_pressed:
            if not self.avatar.jumping or not self.avatar.falling:
                delta_x = PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
        #elif (self.avatar.grounded or self.avatar.laddered) and self.left_pressed and not self.right_pressed:
            if not self.avatar.jumping or not self.avatar.falling:
                delta_x = -PLAYER_MOVEMENT_SPEED
        '''
        else:
            delta_x = 0
        '''

        self.avatar.body.velocity = (delta_x, delta_y)


    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        repeat = event.repeat
        """Called whenever a key is pressed. """
        #if key == arcade.key.UP or key == arcade.key.W:
        if key == sdl.SDLK_w:
            if down:
                self.up_pressed = True
            else:
                self.up_pressed = False
                self.jump_needs_reset = False
        #elif key == arcade.key.DOWN or key == arcade.key.S:
        elif key == sdl.SDLK_s:
            if down:
                self.down_pressed = True
            else:
                self.down_pressed = False
        #elif key == arcade.key.LEFT or key == arcade.key.A:
        elif key == sdl.SDLK_a:
            if down:
                self.left_pressed = True
            else:
                self.left_pressed = False
        #elif key == arcade.key.RIGHT or key == arcade.key.D:
        elif key == sdl.SDLK_d:
            if down:
                self.right_pressed = True
            else:
                self.right_pressed = False
        #elif key == arcade.key.SPACE:
        elif key == sdl.SDLK_SPACE:
            if down:
                self.avatar.punching = True
            else:
                self.avatar.punching = False

        self.process_keychange()
