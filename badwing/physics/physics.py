import arcade
import pymunk

from badwing.constants import *


class PhysicsMeta(type):

    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Physics:
    def __init__(self, kind):
        self.type = kind

    def setup():
        pass

    def update(self, model, delta_time=1/60.0):
        pass

    def create_body(self, model, offset=None):
        pass


class GroupPhysics(Physics):
    def __init__(self, kind=PT_GROUP):
        super().__init__(kind)

    def setup():
        pass

    def update(self, model, delta_time=1/60.0):
        pass

    def create_body(self, model, offset=None):
        pass

