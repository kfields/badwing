from typing import TYPE_CHECKING

from loguru import logger
import glm

from ....collision_type import CollisionType
from crunge import sdl
from crunge import box2d as b2

from crunge.engine.d2.scene.scene_2d import Scene2D

from crunge.engine.d2.physics import MotionState
from crunge.engine.d2.physics import globe as physics_globe
from crunge.engine.d2.physics.constants import PT_DYNAMIC, PT_KINEMATIC, PT_STATIC

from .... import globe, character
from ....constants import *
from . import CharacterController

if TYPE_CHECKING:
    from ..dynamic_character import DynamicCharacter

MAX_SPEED = 5.0
JUMP_IMPULSE = 4.0
FOOT_FRICTION = 1.2

# New Constants for Air Control
AIR_ACCEL_FORCE = 10.0
AIR_DRAG = 0.95           # Multiplier to slow down horizontal drift when keys are released

# Box2D v3 has no collision_type enum like Chipmunk. We identify the foot
# sensor by shape id equality instead, and mark it via a category bit so it
# can be filtered/queried if needed later.
CATEGORY_FOOT = 0x0002


class DynamicFootSensorHandler:
    """
    Box2D v3 reports contacts via per-frame event polling rather than
    begin/separate callbacks. Call poll(world_id) once per physics step
    (or once per frame, before consumers read touching()/clear() below).
    """

    def __init__(self, foot_shape: b2.Shape):
        self.foot_shape = foot_shape
        self._ground_contacts: list[b2.Shape] = []

    def poll(self, world: b2.World) -> None:
        events = world.get_contact_events()

        for evt in events.get_begin_events():
            logger.debug(f"begin contact event: {evt}, shape_id_a: {evt.shape_id_a.user_data}, shape_id_b: {evt.shape_id_b.user_data}")
            other = self._other_shape(evt.shape_id_a, evt.shape_id_b)
            if other is not None:
                logger.debug(f"begin contact with {other}")
                self._ground_contacts.append(other)

        for evt in events.get_end_events():
            logger.debug(f"end contact event: {evt}, shape_id_a: {evt.shape_id_a.user_data}, shape_id_b: {evt.shape_id_b.user_data}")
            other = self._other_shape(evt.shape_id_a, evt.shape_id_b)
            if other is not None:
                logger.debug(f"end contact with {other}")
                self._ground_contacts = [
                    s for s in self._ground_contacts if s != other
                ]

    def _other_shape(self, a: b2.Shape, b_: b2.Shape):
        if a.user_material == CollisionType.FEET:
            return b_
        if b_.user_material == CollisionType.FEET:
            return a
        return None

    def clear(self) -> None:
        self._ground_contacts.clear()

    def touching(self) -> bool:
        return bool(self._ground_contacts)


class DynamicCharacterController(CharacterController):
    def __init__(self, avatar: "DynamicCharacter"):
        super().__init__(avatar)
        self.world = physics_globe.world
        self.avatar = avatar

        scene = Scene2D.get_current()
        self.character_layer = scene.get_layer("pc")
        self.ground_layer = scene.get_layer("ground")
        self.ladder_layer = scene.get_layer("ladder")

        self._setup_feet_shape()
        self._setup_collision_handlers()

    def _setup_feet_shape(self):
        # avatar.body is a b2BodyId (see PPU/Box2D migration notes:
        # geometry is authored in meters at creation time).
        body = self.avatar.body
        bounds = self.avatar.bounds
        hh = bounds.height / 2

        feet_y = -hh + 0.25

        circle = b2.Circle()
        circle.center = b2.Vec2(0.0, feet_y)
        circle.radius = 0.25

        shape_def = b2.ShapeDef()
        shape_def.material = b2.SurfaceMaterial(friction = FOOT_FRICTION, restitution = 0.0)

        shape_def.is_sensor = False  # feet still need contact response; only
                                     # the *ground layer* would be a sensor
        shape_def.enable_contact_events = True  # required on BOTH shapes

        # Box2D's negative groupIndex gives the
        # same "never collide within group" behavior.
        group = -((id(body) & 0x7FFF) or 1)
        shape_def.filter = b2.Filter()
        shape_def.filter.category_bits = CATEGORY_FOOT
        shape_def.filter.group_index = group

        self.feet_shape = b2.create_circle_shape(body, shape_def, circle)
        self.feet_shape.user_data = self
        self.feet_shape.user_material = CollisionType.FEET

        # Also apply the same never-collide-with-self group to the body's
        # existing shape (avatar.shapes[0] -> avatar.shape_ids[0]).
        main_shape = self.avatar.shapes[0]
        main_filter = main_shape.get_filter()
        main_filter.group_index = group
        #b2.Shape_SetFilter(main_shape_id, main_filter)
        main_shape.set_filter(main_filter)
        # Ground/other shapes in this pair must also opt in:
        # enableContactEvents = True is needed on the *other* shape too,
        # wherever ground/kinematic shapes are created.

    def _setup_collision_handlers(self):
        self._foot_handler = DynamicFootSensorHandler(self.feet_shape)

    def check_grounded(self) -> bool:
        return self._foot_handler.touching()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def mount(self):
        hit_list = self.character_layer.query_intersection(self.avatar.bounds)
        for node in hit_list:
            if isinstance(node, character.Skateboard):
                mount = node
                mount.mount(self.avatar)
                globe.screen.push_avatar(mount)

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

        # 0. Pull this frame's contact events before reading grounded state.
        world = self.world
        self._foot_handler.poll(world)

        # 1. State Transitions
        avatar = self.avatar
        body = avatar.body
        velocity = body.linear_velocity
        vy_threshold = 0.1

        match avatar.motion_state:
            case MotionState.GROUNDED:
                pass  # Handled below

            case MotionState.JUMPING:
                if velocity.y < -vy_threshold:
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
        target_vx = 0
        if self.left_pressed:
            target_vx = -MAX_SPEED
        elif self.right_pressed:
            target_vx = MAX_SPEED

        body = self.avatar.body
        velocity = body.linear_velocity
        body.linear_velocity = b2.Vec2(target_vx, velocity.y)

    def _apply_ladder_movement(self):
        """Direct velocity control + Gravity Cancel"""
        dx = dy = 0
        if self.up_pressed: dy = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed: dy = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed: dx = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed: dx = PLAYER_MOVEMENT_SPEED

        body = self.avatar.body
        world = self.world
        gravity = world.get_gravity()
        mass = body.get_mass()

        body.apply_force_to_center(
            b2.Vec2(0.0, -gravity.y * mass), True
        )
        body.linear_velocity = b2.Vec2(dx, dy)

    def _apply_falling_movement(self):
        """
        Applies forces for air control.
        Includes a drag factor so you don't slide on ice forever in the air.
        """
        body = self.avatar.body
        velocity = body.linear_velocity
        vx, vy = velocity.x, velocity.y

        # 1. Apply Horizontal Force (if below max speed)
        if self.left_pressed and vx > -MAX_SPEED:
            body.apply_force_to_center(b2.Vec2(-AIR_ACCEL_FORCE, 0.0), True)

        elif self.right_pressed and vx < MAX_SPEED:
            body.apply_force_to_center(b2.Vec2(AIR_ACCEL_FORCE, 0.0), True)

        # 2. Apply Air Drag (if no keys pressed)
        if not self.left_pressed and not self.right_pressed:
            body.linear_velocity = b2.Vec2(vx * AIR_DRAG, vy)

    def process_keychange(self):
        avatar = self.avatar
        body = avatar.body
        velocity = body.linear_velocity

        match self.avatar.motion_state:
            case MotionState.GROUNDED:
                if self.up_pressed:
                    if self.check_ladder():
                        avatar.motion_state = MotionState.CLIMBING
                    else:
                        avatar.motion_state = MotionState.JUMPING
                        body.linear_velocity = b2.Vec2(velocity.x, 0.0)
                        point = self.avatar.position
                        world_point = b2.Vec2(point.x, point.y)
                        body.apply_linear_impulse(b2.Vec2(0.0, JUMP_IMPULSE), world_point, True)
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