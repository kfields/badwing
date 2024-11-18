from badwing.level import TileLevel

class Level1(TileLevel):
    @classmethod
    def produce(self):
        level = Level1('level1')
        #level.create()
        return level
        
    #next level
    def get_next_level(self):
        import badwing.scenes.end
        return badwing.scenes.end.EndScreen
