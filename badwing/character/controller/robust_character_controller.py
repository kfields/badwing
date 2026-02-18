from typing import TYPE_CHECKING
from loguru import logger
import pymunk
import glm

from crunge import sdl
from crunge.engine.d2.physics.physics import MotionState
import crunge.engine.d2.physics.globe as physics_globe
from crunge.engine.d2.physics.constants import PT_DYNAMIC, PT_KINEMATIC, PT_STATIC

import badwing.globe
from badwing.constants import *
from badwing.character.controller import CharacterController

if TYPE_CHECKING:
    from badwing.characters.avatar import Avatar

# Tuning
MOVE_SPEED = 512
JUMP_IMPULSE = PLAYER_JUMP_SPEED
ACCEL_AIR = 2000    # Air control force
ACCEL_GROUND = 4500 # Ground control force
#ACCEL_GROUND = 100000 # Ground control force
FRICTION_GROUND = 0.85 # Damping on ground (0.0-1.0)
FRICTION_AIR = 0.98    # Damping in air (drag)
JUMP_FORCE = PLAYER_JUMP_SPEED
GRAVITY_GRAVITATION = 1.0 # Multiplier for gravity

# How far to look for ground (pixels)
#GROUND_CHECK_DIST = 4.0 
GROUND_CHECK_DIST = 8.0 
# Radius of the foot sensor (slightly smaller than body width)
FOOT_RADIUS = 32

class RobustCharacterController(CharacterController):
    def __init__(self, avatar: "Avatar"):
        super().__init__(avatar)
        self.physics_engine = physics_globe.physics_engine
        self.avatar = avatar

        # 2. Setup Layers
        self.character_layer = badwing.globe.scene.character_layer
        self.ground_layer = badwing.globe.scene.ground_layer
        self.ladder_layer = badwing.globe.scene.ladder_layer

        # 3. State
        self.ground_normal = glm.vec2(0, 1)
        self.is_grounded = False
        
        # We NO LONGER need physical foot segments.
        # The main body collider (circle/box) is enough.

    def update(self, delta_time: float):
        super().update(delta_time)
        
        # 1. Continuous Ground Check
        self._check_ground()
        
        # 2. Update State Machine
        self._update_state()

        # 3. Apply Movement Forces
        self._apply_movement()

    def _check_ground(self):
        """
        Performs a Shape Query (Circle Cast) downwards to find the ground.
        This is much more reliable than collision callbacks.
        """
        body = self.avatar.body
        space = self.physics_engine.space
        
        # Position for the sensor (bottom of the character)
        feet_pos = body.position + pymunk.Vec2d(0, -self.avatar.height/2)
        
        # Create a virtual circle for the query
        # We cast it slightly downwards to see if we are standing on something
        query_pos = feet_pos - pymunk.Vec2d(0, GROUND_CHECK_DIST)
        
        # Filter: Don't detect ourselves
        # (Assuming group 1 is the player, change if your setup differs)
        group = (id(body) & 0x7FFFFFFF) or 1
        filt = pymunk.ShapeFilter(group=group)
        #self.avatar.shapes[0].filter = filt
        
        info = space.point_query_nearest(query_pos, FOOT_RADIUS, filt)
        
        if info and info.distance < 0:
            # We are touching ground!
            self.is_grounded = True
            self.ground_normal = glm.vec2(info.gradient.x, info.gradient.y)
            
            # Snap to ground: If we are slightly floating, pull us down smoothly
            # (Optional, but makes slopes feel glued)
            if info.distance > -GROUND_CHECK_DIST:
                body.position += pymunk.Vec2d(0, -info.distance * 0.1)
        else:
            self.is_grounded = False
            self.ground_normal = glm.vec2(0, 1) # Default up

    def _update_state(self):
        avatar = self.avatar
        vy = avatar.body.velocity.y

        match avatar.motion_state:
            case MotionState.GROUNDED:
                if not self.is_grounded:
                    avatar.motion_state = MotionState.FALLING
                elif self.up_pressed and self.check_ladder():
                     avatar.motion_state = MotionState.CLIMBING
                elif self.up_pressed: # Jump
                     self._jump()
                elif self.down_pressed:
                    self.mount()


            case MotionState.JUMPING:
                if vy < 0: avatar.motion_state = MotionState.FALLING
                if self.check_ladder(): avatar.motion_state = MotionState.CLIMBING

            case MotionState.FALLING:
                if self.is_grounded: avatar.motion_state = MotionState.GROUNDED
                elif self.check_ladder() and self.up_pressed: avatar.motion_state = MotionState.CLIMBING
            
            case MotionState.CLIMBING:
                if not self.check_ladder(): avatar.motion_state = MotionState.FALLING

    def _jump(self):
        self.avatar.motion_state = MotionState.JUMPING
        # Reset vertical velocity for consistent jump height
        vx, _ = self.avatar.body.velocity
        self.avatar.body.velocity = (vx, JUMP_IMPULSE)
        # Push slightly away from ground normal if on a slope
        # self.avatar.body.apply_impulse_at_local_point((0, JUMP_IMPULSE))

    def _apply_movement(self):
        body = self.avatar.body
        vx, vy = body.velocity
        
        # --- 1. Ladder Logic ---
        if self.avatar.motion_state == MotionState.CLIMBING:
            dx = dy = 0
            if self.up_pressed: dy = MOVE_SPEED
            elif self.down_pressed: dy = -MOVE_SPEED
            if self.left_pressed: dx = -MOVE_SPEED
            elif self.right_pressed: dx = MOVE_SPEED
            
            # Cancel Gravity
            gx, gy = self.physics_engine.space.gravity
            body.apply_force_at_local_point((0, -gy * body.mass))
            body.velocity = (dx, dy)
            return

        # --- 2. Horizontal Movement ---
        target_vx = 0
        if self.left_pressed: target_vx = -MOVE_SPEED
        elif self.right_pressed: target_vx = MOVE_SPEED

        # Acceleration / Deceleration
        # We manually interpolate velocity instead of using friction.
        # This gives "tight" controls.
        
        if self.is_grounded:
            # Ground Movement
            # Interpolate current X velocity towards target X
            new_vx = vx + (target_vx - vx) * (1.0 - FRICTION_GROUND)
        else:
            # Air Control
            if target_vx != 0:
                 # Add force if pressing keys
                 new_vx = vx + (target_vx * 0.05) # Gentle air strafe
                 # Clamp air speed
                 new_vx = max(-MOVE_SPEED, min(MOVE_SPEED, new_vx))
            else:
                 # Air Drag
                 new_vx = vx * FRICTION_AIR

        body.velocity = (new_vx, vy)

    # ... (Keep Input / Helper methods like check_ladder same as before)
    def check_ladder(self):
        if self.ladder_layer:
            hit_list = self.ladder_layer.query_intersection(self.avatar.bounds)
            if hit_list: return True
        return False

    def mount(self):
        hit_list = self.character_layer.query_intersection(self.avatar.bounds)
        for node in hit_list:
            if isinstance(node, badwing.characters.Skateboard):
                mount = node
                mount.mount(self.avatar)
                badwing.globe.screen.push_avatar(mount)

    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        
        match key:
            case sdl.SDLK_w: self.up_pressed = down
            case sdl.SDLK_s: self.down_pressed = down
            case sdl.SDLK_a: self.left_pressed = down
            case sdl.SDLK_d: self.right_pressed = down