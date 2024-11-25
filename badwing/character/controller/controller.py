from badwing.controller import Controller

class CharacterController(Controller):
    def __init__(self, node=None, passthrough=None):
        super().__init__(passthrough)
        self.node = node
