from .controller.robust_character_controller import RobustCharacterController
from .dynamic_character import DynamicCharacter

class RobustCharacter(DynamicCharacter):
    def control(self):
        return RobustCharacterController(self)
