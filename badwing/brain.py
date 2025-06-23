from crunge.engine.base import Base
from crunge.engine.d2 import Node2D

class Brain(Base):
    def __init__(self):
        super().__init__()
        self.node: Node2D = None

    @property
    def sprite(self):
        return self.node.model

    @sprite.setter
    def sprite(self, val):
        if self.node.model != val:
            self.node.model = val

    @property
    def position(self):
        return self.node.position

    @position.setter
    def position(self, val):
        self.node.position = val

    @property
    def velocity(self):
        return self.node.velocity
    
    @velocity.setter
    def velocity(self, val):
        self.node.velocity = val

    def update(self, delta_time: float):
        pass
