from loguru import logger

from crunge import sdl
import crunge.engine.d2.physics.globe as physics_globe

import badwing.app
from badwing.constants import *

from badwing.character.controller import CharacterController

class KinematicController(CharacterController):
    def __init__(self, pc):
        super().__init__(pc)
        self.physics_engine = physics_globe.physics_engine
        self.pc = pc
        self.pc_sprite = pc.vu
        self.force = (0, 0)
        #self.jump_sound = arcade.load_sound(":resources:/sounds/jump1.wav")
        #
        self.character_layer = badwing.app.scene.character_layer
        self.platforms = badwing.app.scene.ground_layer.sprites
        self.ladders = badwing.app.scene.ladder_layer.sprites

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
        hit_list = arcade.check_for_collision_with_list(self.pc_sprite, self.character_layer.sprites)
        for sprite in hit_list:
            model = sprite.model
            if isinstance(model, badwing.characters.Chassis):
                mount = model.parent
                mount.mount(self.pc)
                badwing.app.scene.push_pc(mount)

    def is_on_ladder(self):
        laddered = self.node.laddered
        if self.ladders:
            hit_list = check_for_collision_with_list(self.pc_sprite, self.ladders)
            if len(hit_list) > 0:
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
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.is_on_ladder():
                delta_y = PLAYER_MOVEMENT_SPEED
            elif self.pc.grounded and not self.jump_needs_reset:
                delta_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                #arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
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
        if self.right_pressed and not self.left_pressed:
            delta_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            delta_x = -PLAYER_MOVEMENT_SPEED
        else:
            delta_x = 0

        self.pc.body.velocity = (delta_x, delta_y)


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
            logger.debug(f"SPACE: {down}")
            if down:
                self.pc.punching = True
            else:
                self.pc.punching = False

        self.process_keychange()
