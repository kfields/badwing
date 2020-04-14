from badwing.avatar import Avatar

class CharacterAvatar(Avatar):
    def __init__(self, model=None, passthrough=None):
        super().__init__(passthrough)
        self.model = model
