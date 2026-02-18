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

MOVE_FORCE = 60_000
MAX_SPEED = 512
JUMP_IMPULSE = PLAYER_JUMP_SPEED
FOOT_FRICTION = 1.2
COYOTE_FRAMES = 6
JUMP_BUFFER = 8

CT_FOOT = 9
CT_FOOT_SENSOR = 10


class DynamicFootSensorHandler:
    def __init__(self, space: pymunk.Space):
        self._ground_contacts: list[pymunk.Shape] = []

        space.on_collision(CT_FOOT, PT_STATIC, begin=self.begin, separate=self.separate)
        space.on_collision(
            CT_FOOT, PT_KINEMATIC, begin=self.begin, separate=self.separate
        )

    def begin(self, arbiter, space, data):
        logger.debug("Foot sensor began contact")
        a, b = arbiter.shapes
        other = b if a.collision_type == CT_FOOT else a
        self._ground_contacts.append(other)
        return True

    def separate(self, arbiter, space, data):
        logger.debug("Foot sensor ended contact")
        a, b = arbiter.shapes
        other = b if a.collision_type == CT_FOOT else a
        # self._ground_contacts.remove(other)
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

        self.character_layer = badwing.globe.scene.character_layer
        self.ground_layer = badwing.globe.scene.ground_layer
        self.ladder_layer = badwing.globe.scene.ladder_layer

        self._setup_foot_shapes()
        self._setup_upright_constraint()
        self._setup_collision_handlers()

    # ------------------------------------------------------------------
    # Foot shapes: 2 physical feet + 1 dedicated sensor
    # ------------------------------------------------------------------
    def _setup_foot_shapes(self):
        body = self.avatar.body
        bounds = self.avatar.bounds
        hw = bounds.width / 2
        hh = bounds.height / 2

        foot_y = -hh
        foot_y_offset = 16
        foot_inset = 16
        foot_toe = hw + 16

        # Physical feet (these provide friction + surface_velocity “conveyor belt”)
        self.foot_l = pymunk.Segment(
            body, (-foot_inset, foot_y), (-foot_toe, foot_y - foot_y_offset), radius=10
        )
        self.foot_r = pymunk.Segment(
            body, (foot_inset, foot_y), (foot_toe, foot_y - foot_y_offset), radius=10
        )
        for foot in (self.foot_l, self.foot_r):
            foot.friction = FOOT_FRICTION
            foot.elasticity = 0.0
            foot.collision_type = CT_FOOT  # NOT the sensor type

        # Optional: put all “self” shapes into the same non-colliding group
        # so feet/sensor never collide with the avatar's own main collider.
        # (Only if you have a separate main collider shape on the same body.)
        group = (id(body) & 0x7FFFFFFF) or 1
        filt = pymunk.ShapeFilter(group=group)
        self.foot_l.filter = filt
        self.foot_r.filter = filt
        self.avatar.shapes[0].filter = filt

        self.physics_engine.space.add(self.foot_l, self.foot_r)

    # ------------------------------------------------------------------
    # Upright constraint: static anchor + motor(rate=0)
    # Much more stable than pivot+gear with odd anchors/ratio.
    # ------------------------------------------------------------------
    def _setup_upright_constraint(self):
        space = self.physics_engine.space
        body = self.avatar.body

        # Keep this static body positioned under the character each frame.
        self.static_pivot = pymunk.Body(body_type=pymunk.Body.STATIC)

        # Motor tries to keep relative angular velocity at 0.
        self.upright_motor = pymunk.SimpleMotor(self.static_pivot, body, 0.0)
        self.upright_motor.max_force = 800_000  # tune: lower if it feels too “locked”

        # Also prevent drift in angle by softly springing toward 0 relative angle.
        # (Optional but helps if torques accumulate.)
        self.upright_spring = pymunk.DampedRotarySpring(
            self.static_pivot,
            body,
            rest_angle=0.0,
            stiffness=2_000_000,
            damping=200_000,
        )

        space.add(self.upright_motor, self.upright_spring)

    def _setup_collision_handlers(self):
        space = self.physics_engine.space
        self._foot_handler = DynamicFootSensorHandler(space)

    def check_grounded(self) -> bool:
        return self._foot_handler.touching()

    # ------------------------------------------------------------------
    # Helpers (unchanged)
    # ------------------------------------------------------------------
    def mount(self):
        logger.debug(f"avatar bounds: {self.avatar.bounds}")
        hit_list = self.character_layer.query_intersection(self.avatar.bounds)
        for node in hit_list:
            logger.debug(f"Checking {node}")
            if isinstance(node, badwing.characters.Skateboard):
                logger.debug(f"Mounting {node}")
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

        # 1. Update Pivot
        p = glm.vec2(self.avatar.body.position.x, self.avatar.body.position.y)
        self.static_pivot.position = (p.x, p.y)

        # 2. Handle State Transitions (Logic triggers)
        avatar = self.avatar
        body = avatar.body
        vx, vy = body.velocity
        vy_threshold = 0.1

        match avatar.motion_state:
            case MotionState.GROUNDED:
                pass

            case MotionState.JUMPING:
                if vy < -vy_threshold:
                    logger.debug("Jumping -> Falling")
                    avatar.motion_state = MotionState.FALLING
                # Allow catching ladder mid-jump
                if self.check_ladder():
                    avatar.motion_state = MotionState.CLIMBING

            case MotionState.CLIMBING:
                if not self.check_ladder():
                    logger.debug("Climbing -> Falling")
                    avatar.motion_state = MotionState.FALLING

            case MotionState.FALLING:
                if self.check_grounded():
                    logger.debug("Falling -> Grounded")
                    avatar.motion_state = MotionState.GROUNDED
                # Allow catching ladder while falling
                elif self.check_ladder() and self.up_pressed:
                    avatar.motion_state = MotionState.CLIMBING

        # 3. Continuous Physics Application
        if avatar.motion_state == MotionState.GROUNDED:
            self._apply_ground_movement()
        elif avatar.motion_state == MotionState.CLIMBING:
            self._apply_ladder_movement()

        # 4. Cleanup Sensors
        self._foot_handler.clear()

    def _apply_ground_movement(self):
        """Calculates target velocity based on held keys and applies to feet."""
        target_vx = 0
        if self.left_pressed:
            target_vx = -MAX_SPEED
        elif self.right_pressed:
            target_vx = MAX_SPEED

        self.foot_l.surface_velocity = (-target_vx, 0)
        self.foot_r.surface_velocity = (-target_vx, 0)

    def _apply_ladder_movement(self):
        """Cancels gravity and applies direct velocity for climbing."""
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

        # Cancel gravity so we don't slide down
        gx, gy = self.physics_engine.space.gravity
        body.apply_force_at_local_point((0, -gy * body.mass))

        # Apply velocity directly
        body.velocity = (dx, dy)

    def process_keychange(self):
        """
        Only handle one-shot events here (Jumping, Mounting).
        Continuous movement (Walking, Climbing) is now handled in update().
        """
        avatar = self.avatar
        body = avatar.body
        vx, vy = body.velocity

        match self.avatar.motion_state:
            case MotionState.GROUNDED:
                if self.up_pressed:
                    if self.check_ladder():
                        avatar.motion_state = MotionState.CLIMBING
                    else:
                        logger.debug("Grounded -> Jumping")
                        avatar.motion_state = MotionState.JUMPING
                        body.velocity = (vx, 0)
                        body.apply_impulse_at_local_point((0, JUMP_IMPULSE))
                        self.jump_needs_reset = True
                elif self.down_pressed:
                    self.mount()

            case MotionState.CLIMBING:
                # Logic moved to _apply_ladder_movement and update
                pass

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        repeat = event.repeat
        logger.debug(f"Key event: key={key}, down={down}, repeat={repeat}")

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
