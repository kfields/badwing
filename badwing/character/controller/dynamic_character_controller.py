from typing import TYPE_CHECKING

from loguru import logger
import pymunk
import glm

from crunge import sdl
from crunge.engine.d2.physics.physics import MotionState
import crunge.engine.d2.physics.globe as physics_globe
from crunge.engine.d2.physics.constants import PT_DYNAMIC, PT_KINEMATIC, PT_STATIC
from crunge.engine.d2.node_2d import Node2D

import badwing.globe
from badwing.constants import *
from badwing.character.controller import CharacterController

if TYPE_CHECKING:
    from badwing.characters.avatar import Avatar

MAX_SPEED = 512
JUMP_IMPULSE = PLAYER_JUMP_SPEED
FOOT_FRICTION = 1.2

# New Constants for Air Control
AIR_ACCEL_FORCE = 20_000  # Force applied when pressing keys in air
AIR_DRAG = 0.95           # Multiplier to slow down horizontal drift when keys are released

CT_FOOT = 9


class DynamicFootSensorHandler:
    def __init__(self, space: pymunk.Space):
        self._ground_contacts: list[pymunk.Shape] = []

        space.on_collision(CT_FOOT, PT_STATIC, begin=self.begin, separate=self.separate)
        space.on_collision(
            CT_FOOT, PT_KINEMATIC, begin=self.begin, separate=self.separate
        )
        space.on_collision(
            CT_FOOT, PT_DYNAMIC, begin=self.begin, separate=self.separate
        )

    def begin(self, arbiter, space, data):
        # logger.debug("Foot sensor began contact")
        a, b = arbiter.shapes
        other = b if a.collision_type == CT_FOOT else a
        self._ground_contacts.append(other)
        return True

    def separate(self, arbiter, space, data):
        # logger.debug("Foot sensor ended contact")
        # Contact removal handled by clear()
        return None

    def clear(self) -> None:
        self._ground_contacts.clear()

    def touching(self) -> bool:
        return bool(self._ground_contacts)


class DynamicCharacterController(CharacterController):
    def __init__(self, avatar: "Avatar"):
        super().__init__(avatar)
        self.physics_engine = physics_globe.physics_engine
        self.avatar = avatar

        # Infinite Inertia: Locks rotation so character stays upright
        #self.avatar.body.moment = float('inf')

        self.character_layer = badwing.globe.scene.character_layer
        self.ground_layer = badwing.globe.scene.ground_layer
        self.ladder_layer = badwing.globe.scene.ladder_layer

        self._setup_foot_shapes()
        self._setup_collision_handlers()

    def _setup_foot_shapes(self):
        body = self.avatar.body
        bounds = self.avatar.bounds
        hw = bounds.width / 2
        hh = bounds.height / 2

        foot_y = -hh
        foot_y_offset = 16
        foot_inset = 16
        foot_toe = hw + 16

        self.foot_l = pymunk.Segment(
            body, (-foot_inset, foot_y), (-foot_toe, foot_y - foot_y_offset), radius=10
        )
        self.foot_r = pymunk.Segment(
            body, (foot_inset, foot_y), (foot_toe, foot_y - foot_y_offset), radius=10
        )
        for foot in (self.foot_l, self.foot_r):
            foot.friction = FOOT_FRICTION
            foot.elasticity = 0.0
            foot.collision_type = CT_FOOT

        group = (id(body) & 0x7FFFFFFF) or 1
        filt = pymunk.ShapeFilter(group=group)
        self.foot_l.filter = filt
        self.foot_r.filter = filt
        self.avatar.shapes[0].filter = filt

        self.physics_engine.space.add(self.foot_l, self.foot_r)

    def _setup_collision_handlers(self):
        space = self.physics_engine.space
        self._foot_handler = DynamicFootSensorHandler(space)

    def check_grounded(self) -> bool:
        return self._foot_handler.touching()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
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
                pass # Handled below

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
        self.foot_r.surface_velocity = (-target_vx, 0)

    def _apply_ladder_movement(self):
        """Direct velocity control + Gravity Cancel"""
        dx = dy = 0
        if self.up_pressed: dy = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed: dy = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed: dx = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed: dx = PLAYER_MOVEMENT_SPEED

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
            case sdl.SDLK_w: self.up_pressed = down
            case sdl.SDLK_s: self.down_pressed = down
            case sdl.SDLK_a: self.left_pressed = down
            case sdl.SDLK_d: self.right_pressed = down
            case sdl.SDLK_SPACE: self.avatar.punching = down

        self.process_keychange()