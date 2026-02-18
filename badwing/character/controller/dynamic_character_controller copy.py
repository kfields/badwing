from loguru import logger
import glm

from crunge import sdl
from crunge.engine.d2.physics.kinematic import MotionState
import crunge.engine.d2.physics.globe as physics_globe
from crunge.engine.d2.node_2d import Node2D
import badwing.globe
from badwing.constants import *

from badwing.character.controller import CharacterController


class DynamicCharacterController(CharacterController):
    def __init__(self, avatar: Node2D):
        super().__init__(avatar)
        self.physics_engine = physics_globe.physics_engine
        self.avatar = avatar
        # self.jump_sound = arcade.load_sound(":resources:/sounds/jump1.wav")
        #
        self.character_layer = badwing.globe.scene.character_layer
        self.ground_layer = badwing.globe.scene.ground_layer
        self.ladder_layer = badwing.globe.scene.ladder_layer

    def mount(self):
        logger.debug(f"avatar bounds: {self.avatar.bounds}")
        hit_list = self.character_layer.query_intersection(self.avatar.bounds)
        for node in hit_list:
            logger.debug(f"Checking {node}")
            # if isinstance(node, badwing.characters.Chassis):
            if isinstance(node, badwing.characters.Skateboard):
                logger.debug(f"Mounting {node}")
                # mount = node.group
                mount = node
                mount.mount(self.avatar)
                badwing.globe.screen.push_avatar(mount)

    def check_ladder(self):
        if self.ladder_layer:
            hit_list = self.ladder_layer.query_intersection(self.avatar.bounds)
            if len(hit_list) > 0:
                # logger.debug(f"on ladder: {hit_list}")
                logger.debug(f"avatar bounds: {self.avatar.bounds}")
                for node in hit_list:
                    logger.debug(f"bounds: {node.bounds}")

                return True
        return False

    def process_keychange(self):
        delta = glm.vec2(0, 0)

        match self.avatar.motion_state:
            case MotionState.GROUNDED:
                logger.debug("Grounded")
                if self.left_pressed:
                    delta.x -= PLAYER_MOVEMENT_SPEED
                elif self.right_pressed and not self.left_pressed:
                    delta.x += PLAYER_MOVEMENT_SPEED

                if self.up_pressed:
                    if self.check_ladder():
                        self.avatar.motion_state = MotionState.CLIMBING
                        delta.y = PLAYER_MOVEMENT_SPEED
                    else:
                        logger.debug("Grounded -> Jumping")
                        self.avatar.motion_state = MotionState.JUMPING
                        self.jump_needs_reset = True
                        delta.y = PLAYER_JUMP_SPEED
                    # arcade.play_sound(self.jump_sound)
                elif self.down_pressed:
                    self.mount()

            case MotionState.JUMPING:
                logger.debug("Jumping")
                if self.check_ladder():
                    logger.debug("On ladder, resetting to climbing")
                    self.avatar.motion_state = MotionState.CLIMBING

                if self.right_pressed:
                    delta.x += PLAYER_MOVEMENT_SPEED
                elif self.left_pressed:
                    delta.x -= PLAYER_MOVEMENT_SPEED

                self.avatar.motion_state = MotionState.FALLING

            case MotionState.CLIMBING:
                logger.debug("Climbing")
                if not self.check_ladder():
                    logger.debug("Not on ladder, resetting to grounded")
                    self.avatar.motion_state = MotionState.FALLING
                if self.up_pressed:
                    delta.y = PLAYER_MOVEMENT_SPEED
                elif self.down_pressed:
                    delta.y -= PLAYER_MOVEMENT_SPEED

                if self.left_pressed:
                    delta.x -= PLAYER_MOVEMENT_SPEED
                elif self.right_pressed:
                    delta.x += PLAYER_MOVEMENT_SPEED

            case MotionState.FALLING:
                logger.debug("Falling")
                if self.check_ladder():
                    logger.debug("On ladder, resetting to climbing")
                    self.avatar.motion_state = MotionState.CLIMBING

                if self.left_pressed:
                    delta.x -= PLAYER_MOVEMENT_SPEED
                elif self.right_pressed:
                    delta.x += PLAYER_MOVEMENT_SPEED

        self.avatar.body.velocity = tuple(delta)

    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        repeat = event.repeat

        if self.avatar.falling and repeat:
            # If the avatar is falling, we don't want to process key repeats
            return

        match key:
            case sdl.SDLK_w:
                self.up_pressed = down
            case sdl.SDLK_s:
                self.down_pressed = down
            case sdl.SDLK_a:
                self.left_pressed = down
            case sdl.SDLK_d:
                self.right_pressed = down
            case sdl.SDLK_SPACE:
                self.avatar.punching = down

        self.process_keychange()
