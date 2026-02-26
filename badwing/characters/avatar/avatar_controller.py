from typing import TYPE_CHECKING

from loguru import logger
import pymunk
import glm

from crunge import sdl
from crunge.engine.d2.physics.physics import MotionState
import crunge.engine.d2.physics.globe as physics_globe
from crunge.engine.d2.physics.constants import PT_DYNAMIC, PT_KINEMATIC, PT_STATIC
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.entity.character.controller import DynamicCharacterController

import badwing.globe
from badwing.constants import *

if TYPE_CHECKING:
    from .avatar import Avatar

MAX_SPEED = 512
JUMP_IMPULSE = PLAYER_JUMP_SPEED
FOOT_FRICTION = 1.2

# New Constants for Air Control
# AIR_ACCEL_FORCE = 20_000  # Force applied when pressing keys in air
AIR_ACCEL_FORCE = 10_000  # Force applied when pressing keys in air
AIR_DRAG = 0.95  # Multiplier to slow down horizontal drift when keys are released

CT_FOOT = 9


class AvatarController(DynamicCharacterController):
    def __init__(self, avatar: "Avatar"):
        super().__init__(avatar)
        self.avatar = avatar

        self.character_layer = badwing.globe.scene.character_layer
        self.ground_layer = badwing.globe.scene.ground_layer
        self.ladder_layer = badwing.globe.scene.ladder_layer

    def mount(self):
        hit_list = self.character_layer.query_intersection(self.avatar.bounds)
        for node in hit_list:
            if isinstance(node, badwing.characters.Skateboard):
                mount = node
                mount.mount(self.avatar)
                badwing.globe.screen.push_avatar(mount)

    def check_ladder(self):
        if self.ladder_layer:
            hit_list = self.ladder_layer.query_intersection(self.avatar.bounds)
            if hit_list:
                return True
        return False

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------

    def update(self, delta_time: float):
        super().update(delta_time)

        # 1. State Transitions
        avatar = self.avatar
        body = avatar.body
        vx, vy = body.velocity
        vy_threshold = 0.1

        match avatar.motion_state:
            case MotionState.GROUNDED:
                pass  # Handled below

            case MotionState.JUMPING:
                if vy < -vy_threshold:
                    avatar.motion_state = MotionState.FALLING
                if self.check_ladder():
                    avatar.motion_state = MotionState.CLIMBING

            case MotionState.CLIMBING:
                if not self.check_ladder():
                    avatar.motion_state = MotionState.FALLING

            case MotionState.FALLING:
                if self.check_grounded():
                    avatar.motion_state = MotionState.GROUNDED
                elif self.check_ladder() and self.up_pressed:
                    avatar.motion_state = MotionState.CLIMBING

        # 2. Continuous Physics Application
        if avatar.motion_state == MotionState.GROUNDED:
            self._apply_ground_movement()

        elif avatar.motion_state == MotionState.CLIMBING:
            self._apply_ladder_movement()

        elif avatar.motion_state in (MotionState.JUMPING, MotionState.FALLING):
            self._apply_falling_movement()

        # 3. Cleanup Sensors
        self._foot_handler.clear()

    def _apply_ground_movement(self):
        """Standard Conveyor Belt movement for feet"""
        target_vx = 0
        if self.left_pressed:
            target_vx = -MAX_SPEED
        elif self.right_pressed:
            target_vx = MAX_SPEED

        self.foot_l.surface_velocity = (-target_vx, 0)
        # self.foot_r.surface_velocity = (-target_vx, 0)

    def _apply_ladder_movement(self):
        """Direct velocity control + Gravity Cancel"""
        dx = dy = 0
        if self.up_pressed:
            dy = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed:
            dy = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed:
            dx = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed:
            dx = PLAYER_MOVEMENT_SPEED

        body = self.avatar.body
        gx, gy = self.physics_engine.space.gravity
        body.apply_force_at_local_point((0, -gy * body.mass))
        body.velocity = (dx, dy)

    def _apply_falling_movement(self):
        """
        Applies forces for air control.
        Includes a drag factor so you don't slide on ice forever in the air.
        """
        body = self.avatar.body
        vx, vy = body.velocity

        # 1. Apply Horizontal Force (if below max speed)
        if self.left_pressed and vx > -MAX_SPEED:
            body.apply_force_at_local_point((-AIR_ACCEL_FORCE, 0))
        elif self.right_pressed and vx < MAX_SPEED:
            body.apply_force_at_local_point((AIR_ACCEL_FORCE, 0))

        # 2. Apply Air Drag (if no keys pressed)
        # This helps precise landing.
        if not self.left_pressed and not self.right_pressed:
            # Simple linear drag on X axis only
            body.velocity = (vx * AIR_DRAG, vy)

    def process_keychange(self):
        avatar = self.avatar
        body = avatar.body
        vx, vy = body.velocity

        match self.avatar.motion_state:
            case MotionState.GROUNDED:
                if self.up_pressed:
                    if self.check_ladder():
                        avatar.motion_state = MotionState.CLIMBING
                    else:
                        avatar.motion_state = MotionState.JUMPING
                        body.velocity = (vx, 0)
                        body.apply_impulse_at_local_point((0, JUMP_IMPULSE))
                        self.jump_needs_reset = True
                elif self.down_pressed:
                    self.mount()
            case _:
                pass

    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down

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
