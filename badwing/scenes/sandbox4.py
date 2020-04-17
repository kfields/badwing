from badwing.level import StickerLevel

class Sandbox(StickerLevel):
    @classmethod
    def create(self):
        level = Sandbox('sandbox4')
        level.setup()
        return level
        
    #next level
    def get_next_level(self):
        import badwing.scenes.level2
        return badwing.scenes.level2.Level2
