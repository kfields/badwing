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
MOVE_FORCE = 6_000
MAX_SPEED = PLAYER_MOVEMENT_SPEED  # reuse your existing constant
JUMP_IMPULSE = PLAYER_JUMP_SPEED  # reuse your existing constant
FOOT_FRICTION = 1.2
COYOTE_FRAMES = 6
JUMP_BUFFER = 8

# Pymunk collision types — make sure these don't clash with your other shapes
CT_DEFAULT = 1
CT_FOOT_SENSOR = 3


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

"""
class DynamicFootSensorHandler(CollisionHandler):
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
"""

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
        foot_y_offset = 32
        #foot_inset = 4
        foot_inset = 32
        #foot_toe = hw + 4
        foot_toe = hw + 32

        import pymunk

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

        space = self.physics_engine.space
        space.add(self.foot_l, self.foot_r)

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
    # Movement — force-based instead of direct velocity assignment
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
            body.apply_impulse_at_local_point((0, -JUMP_IMPULSE))
            self._jump_buffer = 0
            self._coyote_timer = 0

        # --- Horizontal movement via forces ---
        if self.left_pressed and vx > -MAX_SPEED:
            body.apply_force_at_local_point((-MOVE_FORCE, 0))
        elif self.right_pressed and vx < MAX_SPEED:
            body.apply_force_at_local_point((MOVE_FORCE, 0))

        # --- Horizontal damping ---
        # Snappy on ground, floaty in air
        damp = 0.82 if self.on_ground else 0.96
        body.velocity = (vx * damp, body.velocity.y)

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

        # Keep upright (belt-and-suspenders alongside your gear joint)
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
