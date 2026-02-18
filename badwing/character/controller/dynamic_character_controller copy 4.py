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
    def __init__(self, controller: "DynamicCharacterController", space: pymunk.Space, ground_contacts: set[pymunk.Shape]):
        self.controller = controller
        self._ground_contacts = ground_contacts

        space.on_collision(
            CT_FOOT, PT_STATIC, begin=self.begin, separate=self.separate
        )
        space.on_collision(
            CT_FOOT, PT_KINEMATIC, begin=self.begin, separate=self.separate
        )

    def begin(self, arbiter, space, data):
        logger.debug("Foot sensor began contact")
        a, b = arbiter.shapes
        other = b if a.collision_type == CT_FOOT else a
        self._ground_contacts.add(other)
        #self.controller.avatar.motion_state = MotionState.GROUNDED
        return True

    def separate(self, arbiter, space, data):
        logger.debug("Foot sensor ended contact")
        a, b = arbiter.shapes
        other = b if a.collision_type == CT_FOOT else a
        self._ground_contacts.discard(other)
        #self.controller.avatar.motion_state = MotionState.FALLING
        return None


class DynamicCharacterController(CharacterController):
    def __init__(self, avatar: "Avatar"):
        super().__init__(avatar)
        self.physics_engine = physics_globe.physics_engine
        self.avatar = avatar

        self.character_layer = badwing.globe.scene.character_layer
        self.ground_layer = badwing.globe.scene.ground_layer
        self.ladder_layer = badwing.globe.scene.ladder_layer

        self._ground_contacts: set[pymunk.Shape] = set()
        self._coyote_timer = 0
        self._jump_buffer = 0
        self._on_ladder = False

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
            body, (-foot_inset, foot_y), (-foot_toe, foot_y - foot_y_offset), radius=2
        )
        self.foot_r = pymunk.Segment(
            body, (foot_inset, foot_y), (foot_toe, foot_y - foot_y_offset), radius=2
        )
        for foot in (self.foot_l, self.foot_r):
            foot.friction = FOOT_FRICTION
            foot.elasticity = 0.0
            foot.collision_type = CT_FOOT  # NOT the sensor type

        # Dedicated ground sensor (no friction, no impulses; just “am I grounded?”)
        # Place slightly below feet so it catches contact reliably.
        sensor_y = foot_y - 6
        self.foot_sensor = pymunk.Segment(
            body, (-hw * 0.5, sensor_y), (hw * 0.5, sensor_y), radius=2
        )
        self.foot_sensor.sensor = True
        self.foot_sensor.collision_type = CT_FOOT_SENSOR

        # Optional: prevent weird interactions with tiny ledges by increasing sensor radius.
        # self.foot_sensor.radius = 3

        # Optional: put all “self” shapes into the same non-colliding group
        # so feet/sensor never collide with the avatar's own main collider.
        # (Only if you have a separate main collider shape on the same body.)
        group = (id(body) & 0x7FFFFFFF) or 1
        filt = pymunk.ShapeFilter(group=group)
        self.foot_l.filter = filt
        self.foot_r.filter = filt
        self.foot_sensor.filter = filt

        self.physics_engine.space.add(self.foot_l, self.foot_r, self.foot_sensor)

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
            self.static_pivot, body, rest_angle=0.0, stiffness=2_000_000, damping=200_000
        )

        space.add(self.upright_motor, self.upright_spring)

    def _setup_collision_handlers(self):
        space = self.physics_engine.space
        self._foot_handler = DynamicFootSensorHandler(self, space, self._ground_contacts)

    def check_grounded(self) -> bool:
        #value = bool(self._ground_contacts)
        #value = len(self._ground_contacts) != 0
        space = physics_globe.physics_engine.space
        infos = space.shape_query(self.foot_sensor)
        value = len(infos) != 0

        if value:
            self.avatar.motion_state = MotionState.GROUNDED
        else:
            self.avatar.motion_state = MotionState.FALLING

        """
        if value:
            self.avatar.motion_state = MotionState.GROUNDED
        """

        return value

    def update(self, delta_time: float):
        super().update(delta_time)
        # Keep upright anchor following the avatar.
        # Use the BODY position (physics truth), not the render node if they can diverge.
        p = glm.vec2(self.avatar.body.position.x, self.avatar.body.position.y)
        self.static_pivot.position = (p.x, p.y)
        self.check_grounded()

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
    def process_keychange(self):
        body = self.avatar.body
        vx, vy = body.velocity

        # --- Coyote time ---
        if self.avatar.grounded:
            self._coyote_timer = COYOTE_FRAMES
        elif self._coyote_timer > 0:
            self._coyote_timer -= 1

        # --- Ladder check ---
        self._on_ladder = self.check_ladder()

        # --- Ladder climbing ---
        if self._on_ladder:
            dx = dy = 0
            if self.up_pressed:
                dy = PLAYER_MOVEMENT_SPEED
            elif self.down_pressed:
                dy = -PLAYER_MOVEMENT_SPEED
            if self.left_pressed:
                dx = -PLAYER_MOVEMENT_SPEED
            elif self.right_pressed:
                dx = PLAYER_MOVEMENT_SPEED

            # cancel gravity while on ladder
            gx, gy = self.physics_engine.space.gravity
            body.apply_force_at_local_point((0, -gy * body.mass))
            body.velocity = (dx, dy)
            return

        # --- Jump buffer ---
        if self.up_pressed:
            self._jump_buffer = JUMP_BUFFER
        elif self._jump_buffer > 0:
            self._jump_buffer -= 1

        # --- Execute jump ---
        if self.avatar.grounded and self._jump_buffer > 0 and self._coyote_timer > 0:
            logger.debug("Jumping")
            body.velocity = (vx, 0)  # zero vertical before impulse
            body.apply_impulse_at_local_point((0, JUMP_IMPULSE))
            self._jump_buffer = 0
            self._coyote_timer = 0

        # --- Horizontal movement via surface_velocity on FEET ---
        target_vx = 0
        if self.left_pressed:
            target_vx = -MAX_SPEED
        elif self.right_pressed:
            target_vx = MAX_SPEED

        self.foot_l.surface_velocity = (-target_vx, 0)
        self.foot_r.surface_velocity = (-target_vx, 0)

        # --- Air control ---
        if not self.avatar.grounded:
            if self.left_pressed and vx > -MAX_SPEED:
                body.apply_force_at_local_point((-MOVE_FORCE * 0.3, 0))
            elif self.right_pressed and vx < MAX_SPEED:
                body.apply_force_at_local_point((MOVE_FORCE * 0.3, 0))

            body.velocity = (body.velocity.x * 0.96, body.velocity.y)

        # --- Terminal velocity clamp ---
        # If +Y is up and gravity is negative, falling is negative.
        terminal = 2200
        if body.velocity.y < -terminal:
            body.velocity = (body.velocity.x, -terminal)

        # --- Mount ---
        if self.down_pressed and self.avatar.grounded:
            self.mount()

        logger.debug(
            f"{'GROUNDED' if self.avatar.grounded else 'AIRBORNE'} | "
            f"vel=({body.velocity.x:+.0f}, {body.velocity.y:+.0f}) | "
            f"coyote={self._coyote_timer}"
        )

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        repeat = event.repeat

        if self.avatar.falling and repeat:
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
