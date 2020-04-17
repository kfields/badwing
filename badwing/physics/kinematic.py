from arcade import Sprite
from arcade import SpriteList

from badwing.constants import *
from badwing.physics import Physics, PhysicsEngine
from badwing.physics.util import _circular_check, check_grounding

class KinematicPhysics(Physics):
    def __init__(self):
        pass
    def setup():
        pass

    def update(self, delta_time=1/60.0):
        pass

class CollisionHandler:
    def __init__(self, handler):
        self.handler = handler
        handler.begin = lambda arbiter, space, data: self.begin(arbiter, space, data)
        handler.pre_solve = lambda arbiter, space, data: self.pre_solve(arbiter, space, data)
        handler.post_solve = lambda arbiter, space, data: self.post_solve(arbiter, space, data)
        handler.separate = lambda arbiter, space, data: self.separate(arbiter, space, data)

    def begin(self, arbiter, space, data):
        return True

    def pre_solve(self, arbiter, space, data):
        pass

    def post_solve(self, arbiter, space, data):
        pass

    def separate(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kshape.body.model.grounded = False
        pass

class KinematicStaticHandler(CollisionHandler):
    def pre_solve(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kbody = kshape.body
        kbody.model.grounded = True
        velocity = kbody.velocity
        if velocity[1] < 0:
            velocity[1] = 0
        kbody.velocity = velocity

        n = -arbiter.contact_point_set.normal
        penetration = -arbiter.contact_point_set.points[0].distance
        body = arbiter.shapes[1].body
        impulse = arbiter.total_impulse
        position = arbiter.contact_point_set.points[0].point_b
        kbody.position += n * penetration
        return True

class KinematicDynamicHandler(CollisionHandler):

    def pre_solve(self, arbiter, space, data):
        kshape = arbiter.shapes[0]
        kbody = kshape.body
        kmodel = kbody.model
        kmodel.grounded = True

        velocity = kbody.velocity
        if velocity[1] < 0:
            velocity[1] = 0

        normal = -arbiter.contact_point_set.normal
        penetration = -arbiter.contact_point_set.points[0].distance
        body = arbiter.shapes[1].body
        impulse = arbiter.total_impulse
        position = arbiter.contact_point_set.points[0].point_b
        kbody.position += normal * penetration

        impulse = velocity * .005
        impulse[1] = 0
        point = position
        body.apply_impulse_at_local_point(impulse, point)
        kbody.velocity = velocity
        return False

class KinematicPhysicsEngine(PhysicsEngine):
    def __init__(self, k_gravity: float = 0.5):
        super().__init__()
        self.k_gravity = k_gravity

    def setup(self):
        self.kinematic_static_handler = KinematicStaticHandler(self.space.add_collision_handler(PT_KINEMATIC, PT_STATIC))
        self.kinematic_dynamic_handler = KinematicDynamicHandler(self.space.add_collision_handler(PT_KINEMATIC, PT_DYNAMIC))

