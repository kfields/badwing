from badwing.level import TileLevel

class Level1(TileLevel):
    @classmethod
    def create(self):
        level = Level1('level1')
        level.setup()
        return level
        
    #next level
    def get_next_level(self):
        import badwing.scenes.end
        return badwing.scenes.end.EndScreen
        #import badwing.scenes.sandbox
        #return badwing.scenes.sandbox.Sandbox
