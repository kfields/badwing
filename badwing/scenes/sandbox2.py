from badwing.level import StickerLevel

class Sandbox(StickerLevel):
    @classmethod
    def produce(self):
        level = Sandbox('sandbox2')
        level.create()
        return level
        
    #next level
    def get_next_level(self):
        import badwing.scenes.level2
        return badwing.scenes.level2.Level2
