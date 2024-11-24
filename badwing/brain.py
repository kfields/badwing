class Brain:

    @property
    def sprite(self):
        return self.node.sprite

    @sprite.setter
    def sprite(self, val):
        self.node.sprite = val

    @property
    def position(self):
        return self.node.position

    @position.setter
    def position(self, val):
        self.node.position = val

    def __init__(self, node):
        self.node = node

    def update(self, delta_time: float):
        pass