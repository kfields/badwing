from enum import IntEnum
import random

from loguru import logger
import glm

from crunge.engine.math import Bounds2
from crunge.engine.d2.sprite import SpriteVu, SpriteVuGroup

from crunge.engine.d2.entity import Entity2D, EntityGroup2D

from .butterfly_brain import ButterflyBrain


RANGE = 512  # How far they can travel
HALF_RANGE = RANGE / 2
# DEFAULT_BORDER = Bounds2(0, 0, 640, 480)
# DEFAULT_BORDER = Bounds2(0, 0, 1280, 720)
DEFAULT_BORDER = Bounds2(0, 0, 1920, 1080)

class ButterflyKind(IntEnum):
    Aqua = 0
    Blue = 1
    Brown = 2
    Cyan = 3
    Green = 4
    Iridescent = 5
    Red = 6
    Tan = 7
    Teal = 8


class Butterfly(Entity2D):
    def __init__(self, position=glm.vec2(), brain=None, border=DEFAULT_BORDER):
        super().__init__(position, vu=SpriteVu(), brain=brain)
        self.border = border

    @classmethod
    def produce(
        self, kind: ButterflyKind, position=glm.vec2(), border=DEFAULT_BORDER
    ):
        node = kinds[kind].produce(position, border)
        return node

    @classmethod
    def produce_2(self, kind: ButterflyKind, position=glm.vec2()):
        border = Bounds2(
            position.x - HALF_RANGE,
            position.y - HALF_RANGE,
            position.x + HALF_RANGE,
            position.y + HALF_RANGE,
        )
        node = kinds[kind].produce(position, border)
        return node


class ButterflyAqua(Butterfly):
    @classmethod
    def produce(self, position, border=DEFAULT_BORDER):
        brain = ButterflyBrain(8)
        return ButterflyAqua(position, brain, border)


class ButterflyBlue(Butterfly):
    @classmethod
    def produce(self, position, border=DEFAULT_BORDER):
        brain = ButterflyBrain(0)
        return ButterflyBlue(position, brain, border)


class ButterflyBrown(Butterfly):
    @classmethod
    def produce(self, position, border=DEFAULT_BORDER):
        brain = ButterflyBrain(4)
        return ButterflyBrown(position, brain, border)


class ButterflyCyan(Butterfly):
    @classmethod
    def produce(self, position, border=DEFAULT_BORDER):
        brain = ButterflyBrain(5)
        return ButterflyCyan(position, brain, border)


class ButterflyGreen(Butterfly):
    @classmethod
    def produce(self, position, border=DEFAULT_BORDER):
        brain = ButterflyBrain(1)
        return ButterflyGreen(position, brain, border)


class ButterflyIridescent(Butterfly):
    @classmethod
    def produce(self, position, border=DEFAULT_BORDER):
        brain = ButterflyBrain(6)
        return ButterflyIridescent(position, brain, border)


class ButterflyRed(Butterfly):
    @classmethod
    def produce(self, position, border=DEFAULT_BORDER):
        brain = ButterflyBrain(7)
        return ButterflyRed(position, brain, border)


class ButterflyTan(Butterfly):
    @classmethod
    def produce(self, position, border=DEFAULT_BORDER):
        brain = ButterflyBrain(3)
        return ButterflyTan(position, brain, border)


class ButterflyTeal(Butterfly):
    @classmethod
    def produce(self, position, border=DEFAULT_BORDER):
        brain = ButterflyBrain(2)
        return ButterflyTeal(position, brain, border)


kinds = {
    "ButterflyBlue": ButterflyBlue,
    "ButterflyAqua": ButterflyAqua,
    "ButterflyBrown": ButterflyBrown,
    "ButterflyCyan": ButterflyCyan,
    "ButterflyGreen": ButterflyGreen,
    "ButterflyIridescent": ButterflyIridescent,
    "ButterflyRed": ButterflyRed,
    "ButterflyTan": ButterflyTan,
    "ButterflyTeal": ButterflyTeal,
}

kinds_list = list(kinds)


class Butterflies(EntityGroup2D):
    def __init__(self, border=DEFAULT_BORDER):
        super().__init__()

    @classmethod
    def create_random(self, count, border=DEFAULT_BORDER):
        group = Butterflies()
        for i in range(count):
            center_x = random.randint(0, border.right)
            center_y = random.randint(0, border.top)
            position = glm.vec2(center_x, center_y)
            # logger.debug(f"position: {position}")
            ndx = random.randint(0, 8)
            kind = kinds_list[ndx]
            butterfly = Butterfly.produce(kind, position, border)
            group.add_node(butterfly)
        return group
