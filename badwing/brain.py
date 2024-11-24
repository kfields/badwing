from crunge.engine.base import Base


class Brain(Base):
    def __init__(self):
        super().__init__()
        self.node = None

    @property
    def sprite(self):
        return self.node.model

    @sprite.setter
    def sprite(self, val):
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
