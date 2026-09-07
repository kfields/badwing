from loguru import logger
import glm

import crunge.box2d as box2d

from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.entity import EntityGroup2D, Entity2D, DynamicEntity2D
from crunge.engine.d2.physics.geom import BoxGeom, BallGeom
from crunge.engine.d2.physics import globe as physics_globe
from crunge.engine.d2.physics.material import PhysicsMaterial

from ...util import debounce

from .skateboard_controller import SkateboardController

WHEEL_RADIUS = 0.1

# CHASSIS_WIDTH = 0.5
CHASSIS_WIDTH = 1.0
CHASSIS_HEIGHT = 0.1

WHEEL_DENSITY = 1.0
CHASSIS_DENSITY = 1.0

# X_PAD = 0.3
X_PAD = 0
Y_PAD = 0.25

SPEED_DELTA = 0.001
#MAX_SPEED = 0.5
MAX_SPEED = 0.05

# No motor/torque constants any more - propulsion is direct velocity control
# (see update() below), same pattern DynamicCharacterController uses for
# _apply_ground_movement. Wheel joints stay motorless/free-spinning, which
# also removes the reaction-torque path that was causing the pitch wobble.

sprite_loader = SpriteLoader(sprite_builder=CollidableSpriteBuilder())

# Singleton: PhysicsMaterial allocates an id per instance, so constructing
# one per wheel would give the two wheels different ids and grow the registry.
WHEEL_MATERIAL = PhysicsMaterial("skateboard_wheel", friction=0.0, restitution=0.0)


class Wheel(DynamicEntity2D):
    geom = BallGeom(
        radius=WHEEL_RADIUS,
        material=WHEEL_MATERIAL,
        density=WHEEL_DENSITY,
    )

    def __init__(self, position=None):
        sprite = sprite_loader.load("${resources}/items/coinGold.png")
        super().__init__(position, scale=glm.vec2(0.5, 0.5), model=sprite)

    @classmethod
    def produce(cls, position=None):
        return Wheel(position)

DECK_MATERIAL = PhysicsMaterial("skateboard_deck", restitution=0.0)

class Deck(DynamicEntity2D):
    geom = BoxGeom(
        size=glm.vec2(CHASSIS_WIDTH, CHASSIS_HEIGHT),
        material=DECK_MATERIAL,
        density=CHASSIS_DENSITY,
    )

    def __init__(self, position=None):
        sprite = sprite_loader.load("${resources}/tiles/boxCrate.png")
        super().__init__(
            position,
            scale=glm.vec2(1.5, 0.1),
            model=sprite,
        )

    @classmethod
    def produce(cls, position=None):
        return Deck(position)


class Skateboard(EntityGroup2D):
    def __init__(self, position=None):
        super().__init__(position)
        self.mountee = None
        self.mountee_joints = []
        self.speed = 0
        self.front_joint = None
        self.back_joint = None

        chassis_pos = self.position
        self._front_wheel_pos = chassis_pos - glm.vec2(
            -(CHASSIS_WIDTH / 2 + X_PAD), Y_PAD
        )
        self._back_wheel_pos = chassis_pos - glm.vec2(CHASSIS_WIDTH / 2 + X_PAD, Y_PAD)

        self.deck = self.add_node(Deck.produce(chassis_pos))
        self.front_wheel = self.add_node(Wheel.produce(self._front_wheel_pos))
        self.back_wheel = self.add_node(Wheel.produce(self._back_wheel_pos))

        self.add(SkateboardController(self))

    def _created(self):
        super()._created()
        
    @property
    def velocity(self):
        return self.deck.velocity

    @classmethod
    def produce(cls, position=None):
        return Skateboard(position)

    '''
    def control(self):
        return SkateboardController(self)
    '''
    # -- mounting ----------------------------------------------------------

    def mount(self, mountee: Entity2D):
        self.mountee = mountee
        mountee.on_mount(self.deck, glm.vec2(0, 0.6))

        world = physics_globe.world
        weld_def = box2d.WeldJointDef(
            body_id_a=mountee.body,
            body_id_b=self.deck.body,
            local_frame_a=box2d.Transform(p=box2d.Vec2(0, 0)),
            local_frame_b=box2d.Transform(p=box2d.Vec2(0, 0.6)),
        )

        joint = box2d.create_weld_joint(world, weld_def)
        self.mountee_joints = [joint]

    def dismount(self):
        logger.debug("dismounting")
        if self.mountee is None:
            return
        for joint_id in self.mountee_joints:
            box2d.destroy_joint(joint_id)
        self.mountee_joints = []
        self.mountee.on_dismount(self.deck, glm.vec2(0, CHASSIS_HEIGHT / 2))
        self.mountee = None

    # -- joints ------------------------------------------------------------

    def _created(self):
        super()._created()

        world = physics_globe.world
        front_anchor = box2d.Vec2(*(self._front_wheel_pos - self.deck.position))
        back_anchor = box2d.Vec2(*(self._back_wheel_pos - self.deck.position))

        self.front_joint = self._pin_wheel(world, self.front_wheel, front_anchor)
        self.back_joint = self._pin_wheel(world, self.back_wheel, back_anchor)

    def _pin_wheel(self, world, wheel, chassis_anchor):
        joint_def = box2d.RevoluteJointDef(
            body_id_a=wheel.body,
            body_id_b=self.deck.body,
            local_frame_a=box2d.Transform(p=box2d.Vec2(0, 0)),
            local_frame_b=box2d.Transform(p=chassis_anchor),
            # free-spinning; propulsion goes straight to chassis velocity
            enable_motor=False,
        )
        return box2d.create_revolute_joint(world, joint_def)

    def destroy_children(self):
        for joint in (self.front_joint, self.back_joint):
            if joint is not None:
                box2d.destroy_joint(joint)
        self.front_joint = self.back_joint = None
        super().destroy_children()

    '''
    def _destroy(self):
        for joint in (self.front_joint, self.back_joint):
            if joint is not None:
                box2d.destroy_joint(joint)
        self.front_joint = self.back_joint = None
        super()._destroy()
    '''

    # -- propulsion --------------------------------------------------------

    def accelerate(self, rate=SPEED_DELTA):
        self.speed = min(self.speed + rate, MAX_SPEED)

    def decelerate(self, rate=SPEED_DELTA):
        self.speed = max(self.speed - rate, -MAX_SPEED)

    def coast(self):
        self.speed = 0

    @debounce(1)
    def ollie(self, impulse=(0, 1.0), point=(0, 0)):
        logger.debug("ollie")
        self._impulse_at(self.deck, impulse, point)
        if self.mountee:
            self._impulse_at(self.mountee, impulse, point)

    def _impulse_at(self, entity, impulse, point):
        body = entity.body
        world_point = body.get_world_point(box2d.Vec2(*point))
        body.apply_linear_impulse(box2d.Vec2(*impulse), world_point, True)

    def update(self, delta_time=1 / 60):
        super().update(delta_time)
        if not self.speed:
            return
        body = self.deck.body
        angle = body.angle
        forward = glm.vec2(glm.cos(angle), glm.sin(angle))
        impulse = forward * self.speed
        body.apply_linear_impulse_to_center(box2d.Vec2(impulse.x, impulse.y), True)
