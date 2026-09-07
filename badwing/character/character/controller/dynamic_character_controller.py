from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge import sdl
from crunge import box2d as b2

from crunge.engine.d2.scene.scene_2d import Scene2D
from crunge.engine.d2.physics import MotionState
from crunge.engine.d2.physics import globe as physics_globe
from crunge.engine.d2.physics.world import Contact

from .... import globe, character
from ....constants import *
from ....physics_material import FEET
from . import CharacterController

if TYPE_CHECKING:
    from ...avatar import Avatar

MAX_SPEED = 5.0
JUMP_IMPULSE = 2.0

AIR_ACCEL_FORCE = 10.0
AIR_DRAG = 0.95  # slows horizontal drift when keys are released
VY_THRESHOLD = 0.1


class FootSensor:
    """Tracks what the foot shape is standing on.

    Begin/end contacts are edges, not per-frame state: the list persists
    across frames and is only changed when a contact starts or stops.
    """

    def __init__(self, foot_shape: b2.Shape):
        self.foot_shape = foot_shape
        self.contacts: list = []

    def on_contact_began(self, contact: Contact) -> None:
        other = self._other(contact)
        if other is not None:
            self.contacts.append(other)

    def on_contact_ended(self, contact: Contact) -> None:
        other = self._other(contact)
        if other is not None:
            self.contacts = [s for s in self.contacts if s != other]

    def _other(self, contact: Contact):
        # Match this character's own foot shape, not just any FEET material,
        # or another character's feet register here.
        a, b = contact.shape_a, contact.shape_b
        owner = self.foot_shape.user_data
        if a.user_material == FEET.id and a.user_data is owner:
            return b
        if b.user_material == FEET.id and b.user_data is owner:
            return a
        return None

    @property
    def touching(self) -> bool:
        return bool(self.contacts)

    def clear(self) -> None:
        self.contacts.clear()


class DynamicCharacterController(CharacterController):
    def __init__(self, avatar: "Avatar"):
        super().__init__(avatar)
        self.avatar = avatar
        self.world = physics_globe.world
        self.character_layer = None
        self.ground_layer = None
        self.ladder_layer = None

    def _enable(self) -> None:
        super()._enable()
        self.foot_sensor = FootSensor(self._find_foot_shape())
        self.world.contact_began.connect(self.foot_sensor.on_contact_began)
        self.world.contact_ended.connect(self.foot_sensor.on_contact_ended)

    def _ready(self) -> None:
        super()._ready()
        #exit()
        scene = Scene2D.get_current()
        self.character_layer = scene.get_layer("pc")
        self.ground_layer = scene.get_layer("ground")
        self.ladder_layer = scene.get_layer("ladder")

    def _disable(self) -> None:
        self.world.contact_began.disconnect(self.foot_sensor.on_contact_began)
        self.world.contact_ended.disconnect(self.foot_sensor.on_contact_ended)
        super()._disable()

    '''
    def destroy(self) -> None:
        self.world.contact_began.disconnect(self.foot_sensor.on_contact_began)
        self.world.contact_ended.disconnect(self.foot_sensor.on_contact_ended)
        super().destroy()
    '''

    def _find_foot_shape(self) -> b2.Shape:
        for shape in self.avatar.physics.shapes:
            if shape.user_material == FEET.id:
                return shape
        raise ValueError(f"{self.avatar}: no FEET shape; check its geom")

    # -- state -------------------------------------------------------------

    @property
    def physics(self):
        return self.avatar.physics

    def check_grounded(self) -> bool:
        return self.foot_sensor.touching

    def check_ladder(self) -> bool:
        if not self.ladder_layer:
            return False
        return bool(self.ladder_layer.query_intersection(self.avatar.global_bounds))

    def mount(self) -> None:
        for node in self.character_layer.query_intersection(self.avatar.global_bounds):
            if isinstance(node, character.Skateboard):
                node.mount(self.avatar)
                globe.screen.push_avatar(node)
                return

    # -- movement ----------------------------------------------------------

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        avatar = self.avatar
        velocity = self.physics.velocity

        match avatar.motion_state:
            case MotionState.GROUNDED:
                if not self.check_grounded():
                    avatar.motion_state = MotionState.FALLING

            case MotionState.JUMPING:
                if velocity.y < -VY_THRESHOLD:
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

        match avatar.motion_state:
            case MotionState.GROUNDED:
                self._apply_ground_movement()
            case MotionState.CLIMBING:
                self._apply_ladder_movement()
            case MotionState.JUMPING | MotionState.FALLING:
                self._apply_falling_movement()

    def _apply_ground_movement(self) -> None:
        target_vx = 0.0
        if self.left_pressed:
            target_vx = -MAX_SPEED
        elif self.right_pressed:
            target_vx = MAX_SPEED

        velocity = self.physics.velocity
        self.physics.velocity = glm.vec2(target_vx, velocity.y)

    def _apply_ladder_movement(self) -> None:
        """Direct velocity control. The counter-force cancels gravity during
        the step; the velocity write only sets the starting value."""
        dx = dy = 0.0
        if self.up_pressed:
            dy = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed:
            dy = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed:
            dx = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed:
            dx = PLAYER_MOVEMENT_SPEED

        body = self.physics.body
        gravity = self.world.get_gravity()
        mass = body.get_mass()
        self.physics.apply_force(glm.vec2(0.0, -gravity.y * mass))
        self.physics.velocity = glm.vec2(dx, dy)

    '''
    def _apply_ladder_movement(self) -> None:
        """Direct velocity control; setting velocity each frame already
        cancels gravity, so no counter-force is needed."""
        dx = dy = 0.0
        if self.up_pressed:
            dy = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed:
            dy = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed:
            dx = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed:
            dx = PLAYER_MOVEMENT_SPEED

        self.physics.velocity = glm.vec2(dx, dy)
    '''

    def _apply_falling_movement(self) -> None:
        velocity = self.physics.velocity

        if self.left_pressed and velocity.x > -MAX_SPEED:
            self.physics.apply_force(glm.vec2(-AIR_ACCEL_FORCE, 0.0))
        elif self.right_pressed and velocity.x < MAX_SPEED:
            self.physics.apply_force(glm.vec2(AIR_ACCEL_FORCE, 0.0))

        if not self.left_pressed and not self.right_pressed:
            self.physics.velocity = glm.vec2(velocity.x * AIR_DRAG, velocity.y)

    def process_keychange(self) -> None:
        avatar = self.avatar
        if avatar.motion_state is not MotionState.GROUNDED:
            return

        if self.up_pressed:
            if self.check_ladder():
                avatar.motion_state = MotionState.CLIMBING
            else:
                velocity = self.physics.velocity
                self.physics.velocity = glm.vec2(velocity.x, 0.0)
                self.physics.apply_impulse(glm.vec2(0.0, JUMP_IMPULSE))
                avatar.motion_state = MotionState.JUMPING
                self.jump_needs_reset = True
        elif self.down_pressed:
            self.mount()

    def on_key(self, event: sdl.KeyboardEvent) -> None:
        super().on_key(event)
        key, down = event.key, event.down

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
