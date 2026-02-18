from loguru import logger
import pymunk
import glm

from crunge import sdl
import crunge.engine.d2.physics.globe as physics_globe
from crunge.engine.d2.physics.collision import CollisionHandler
from crunge.engine.d2.physics.constants import PT_DYNAMIC, PT_KINEMATIC, PT_STATIC
from crunge.engine.d2.node_2d import Node2D

import badwing.globe
from badwing.constants import *

from badwing.character.controller import CharacterController


# Tuning constants — adjust to taste
MOVE_FORCE = 60_000
#MAX_SPEED = PLAYER_MOVEMENT_SPEED  # reuse your existing constant
MAX_SPEED = 512
JUMP_IMPULSE = PLAYER_JUMP_SPEED  # reuse your existing constant
FOOT_FRICTION = 1.2
COYOTE_FRAMES = 6
JUMP_BUFFER = 8

# Pymunk collision types — make sure these don't clash with your other shapes
CT_DEFAULT = 9
CT_FOOT_SENSOR = 10


class DynamicFootSensorHandler:
    def __init__(self, space: pymunk.Space, ground_contacts: set):
        self._ground_contacts = ground_contacts
        # Register against static AND kinematic ground shapes
        space.on_collision(
            CT_FOOT_SENSOR, PT_STATIC, begin=self.begin, separate=self.separate
        )
        space.on_collision(
            CT_FOOT_SENSOR, PT_KINEMATIC, begin=self.begin, separate=self.separate
        )

    def begin(self, arbiter, space, data):
        for s in arbiter.shapes:
            if s.collision_type != CT_FOOT_SENSOR:
                self._ground_contacts.add(id(s))
        return True

    def separate(self, arbiter, space, data):
        for s in arbiter.shapes:
            if s.collision_type != CT_FOOT_SENSOR:
                self._ground_contacts.discard(id(s))


class DynamicCharacterController(CharacterController):
    def __init__(self, avatar: Node2D):
        super().__init__(avatar)
        self.physics_engine = physics_globe.physics_engine
        self.avatar = avatar

        self.character_layer = badwing.globe.scene.character_layer
        self.ground_layer = badwing.globe.scene.ground_layer
        self.ladder_layer = badwing.globe.scene.ladder_layer

        # Ground / jump state (replaces MotionState machine)
        self._ground_contacts: set[int] = set()
        self._coyote_timer = 0
        self._jump_buffer = 0
        self._on_ladder = False

        self._setup_foot_sensors()
        self._setup_collision_handlers()

    # ------------------------------------------------------------------
    # Foot sensor setup
    # ------------------------------------------------------------------
    def _setup_foot_sensors(self):
        """
        Add two angled segment shapes to the avatar's pymunk body,
        acting as both physical contact points and ground sensors.
        """
        body = self.avatar.body
        bounds = self.avatar.bounds
        hw = bounds.width / 2
        hh = bounds.height / 2

        foot_y = -hh
        foot_y_offset = 16
        foot_inset = 16
        foot_toe = hw + 16

        self.foot_l = pymunk.Segment(
            body, (-foot_inset, foot_y), (-foot_toe, foot_y - foot_y_offset), radius=3
        )
        self.foot_r = pymunk.Segment(
            body, (foot_inset, foot_y), (foot_toe, foot_y - foot_y_offset), radius=3
        )
        for foot in (self.foot_l, self.foot_r):
            foot.friction = FOOT_FRICTION
            foot.elasticity = 0.0
            foot.collision_type = CT_FOOT_SENSOR

        # *** ANTI-ROTATION — THIS IS CRITICAL ***
        # Without this, the character will tumble over
        space = self.physics_engine.space
        self.static_pivot = static_pivot = pymunk.Body(body_type=pymunk.Body.STATIC)
        pivot = pymunk.PivotJoint(static_pivot, body, (-32, -32), (32, -32))
        #pivot = pymunk.PivotJoint(static_pivot, body, tuple(self.avatar.position), tuple(self.avatar.position + glm.vec2(0, -32)))
        pivot.max_bias = 0      # don't correct position
        pivot.max_force = 0     # don't exert position force
        #gear = pymunk.GearJoint(static_pivot, body, 0, 1)
        gear = pymunk.GearJoint(static_pivot, body, 0, 10000)
        gear.max_bias = 0
        #gear.max_force = 8_000  # resist rotation but not rigidly
        gear.max_force = 800_000  # resist rotation but not rigidly

        space.add(self.foot_l, self.foot_r, pivot, gear)

    def _setup_collision_handlers(self):
        space = self.physics_engine.space
        # Pass our ground_contacts set in — the handler mutates it directly
        self._foot_handler = DynamicFootSensorHandler(space, self._ground_contacts)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def on_ground(self) -> bool:
        return bool(self._ground_contacts)

    @property
    def falling(self) -> bool:
        return not self.on_ground and not self._on_ladder

    def update(self, delta_time: float):
        self.static_pivot.position = tuple(self.avatar.position + glm.vec2(0, -32))

    # ------------------------------------------------------------------
    # Existing helpers (unchanged)
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
                logger.debug(f"avatar bounds: {self.avatar.bounds}")
                for node in hit_list:
                    logger.debug(f"bounds: {node.bounds}")
                return True
        return False

    # ------------------------------------------------------------------
    # Movement — surface_velocity + forces hybrid
    # ------------------------------------------------------------------
    def process_keychange(self):
        body = self.avatar.body
        vx, vy = body.velocity

        # --- Coyote time ---
        if self.on_ground:
            self._coyote_timer = COYOTE_FRAMES
        elif self._coyote_timer > 0:
            self._coyote_timer -= 1

        # --- Ladder check ---
        self._on_ladder = self.check_ladder()

        # --- Ladder climbing: direct velocity, suppress gravity ---
        if self._on_ladder:
            logger.debug("Climbing")
            dx = dy = 0
            if self.up_pressed:
                dy = PLAYER_MOVEMENT_SPEED
            elif self.down_pressed:
                dy = -PLAYER_MOVEMENT_SPEED
            if self.left_pressed:
                dx = -PLAYER_MOVEMENT_SPEED
            elif self.right_pressed:
                dx = PLAYER_MOVEMENT_SPEED

            # Zero gravity while on ladder by counteracting it each frame
            body.apply_force_at_local_point(
                (0, -self.physics_engine.space.gravity[1] * body.mass)
            )
            body.velocity = (dx, dy)
            return

        # --- Jump buffer ---
        if self.up_pressed:
            self._jump_buffer = JUMP_BUFFER
        elif self._jump_buffer > 0:
            self._jump_buffer -= 1

        # --- Execute jump ---
        if self._jump_buffer > 0 and self._coyote_timer > 0:
            logger.debug("Jumping")
            body.velocity = (vx, 0)  # zero vertical before impulse
            body.apply_impulse_at_local_point((0, JUMP_IMPULSE))
            self._jump_buffer = 0
            self._coyote_timer = 0

        # --- Horizontal movement using surface_velocity ---
        # This is the key to reducing friction fighting!
        target_vx = 0
        if self.left_pressed:
            target_vx = -MAX_SPEED
        elif self.right_pressed:
            target_vx = MAX_SPEED

        # Negate for surface_velocity: feet push opposite direction
        self.foot_l.surface_velocity = (-target_vx, 0)
        self.foot_r.surface_velocity = (-target_vx, 0)

        # In air, use forces for responsive control (since no friction to leverage)
        if not self.on_ground:
            if self.left_pressed and vx > -MAX_SPEED:
                body.apply_force_at_local_point((-MOVE_FORCE * 0.3, 0))  # weaker air control
            elif self.right_pressed and vx < MAX_SPEED:
                body.apply_force_at_local_point((MOVE_FORCE * 0.3, 0))

        # --- Horizontal damping (lighter now since friction does the work on ground) ---
        if not self.on_ground:
            body.velocity = (vx * 0.96, body.velocity.y)

        # --- Terminal velocity ---
        if body.velocity.y > 2_200:
            body.velocity = (body.velocity.x, 2_200)

        # --- Mount (down key on ground) ---
        if self.down_pressed and self.on_ground:
            self.mount()

        logger.debug(
            f"{'GROUNDED' if self.on_ground else 'AIRBORNE'} | "
            f"vel=({body.velocity.x:+.0f}, {body.velocity.y:+.0f}) | "
            f"coyote={self._coyote_timer}"
        )

        # Keep upright (belt-and-suspenders alongside gear joint)
        body.angular_velocity = 0

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        repeat = event.repeat

        # Skip repeats while airborne (same logic as before)
        if self.falling and repeat:
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