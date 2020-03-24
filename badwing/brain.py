class Brain:

    @property
    def sprite(self):
        return self.model.sprite

    @sprite.setter
    def sprite(self, val):
        self.model.sprite = val

    @property
    def position(self):
        return self.model.position

    @position.setter
    def position(self, val):
        self.model.position = val

    def __init__(self, model):
        self.model = model

    def update(self, delta_time):
        pass