from badwing.controller import Controller

class CharacterController(Controller):
    def __init__(self, model=None, passthrough=None):
        super().__init__(passthrough)
        self.model = model
