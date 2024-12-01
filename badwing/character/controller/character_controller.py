from badwing.level_controller import LevelController

class CharacterController(LevelController):
    def __init__(self, node=None):
        super().__init__()
        self.node = node
