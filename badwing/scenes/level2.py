from badwing.level import TileLevel


class Level2(TileLevel):
    @classmethod
    def produce(self):
        level = Level2('level2')
        level.create()
        return level

    #next level
    def get_next_level(self):
        import badwing.scenes.end
        return badwing.scenes.end.EndScreen
