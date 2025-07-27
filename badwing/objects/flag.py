from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.sprite import SpriteVu


class Pole(Node2D):
    def __init__(self, position, sprite):
        super().__init__(position, vu=SpriteVu(), model=sprite)
        self.collected = False


class Flag(Node2D):
    def __init__(self, position, sprite):
        super().__init__(position, vu=SpriteVu(), model=sprite)
        self.collected = False

    @classmethod
    def produce(self, kind, position, sprite):
        node = kinds[kind].produce(position, sprite)
        return node

    def collect(self):
        #self.destroy()
        return True

class FlagGreen(Flag):
    @classmethod
    def produce(self, position, sprite):
        return FlagGreen(position, sprite)


class FlagYellow(Flag):
    @classmethod
    def produce(self, position, sprite):
        return FlagYellow(position, sprite)


class FlagRed(Flag):
    @classmethod
    def produce(self, position, sprite):
        return FlagRed(position, sprite)


kinds = {
    "Pole": Pole,
    "FlagGreen": FlagGreen,
    "FlagYellow": FlagYellow,
    "FlagRed": FlagRed,
}
