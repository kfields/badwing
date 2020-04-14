import arcade

import badwing.app
import badwing.butterfly
import badwing.flag

class Player:
    def __init__(self):
        badwing.app.player = self
        self.score = 0
        self.on_next_level()
        
    def on_next_level(self):
        self.has_green_flag = False
        self.has_yellow_flag = False
        self.has_red_flag = False
        self.level_beat = False

    def update(self, dt):
        pass

    def collect(self, item):
        if isinstance(item, badwing.butterfly.Butterfly):
            return self.collect_butterfly(item)
        elif isinstance(item, badwing.flag.Flag):
            return self.collect_flag(item)

    def collect_butterfly(self, butterfly):
        self.score +=1
        return True

    def collect_flag(self, flag):
        success = False
        if isinstance(flag, badwing.flag.FlagGreen) and not self.has_green_flag:
            success = self.has_green_flag = flag.collect()
        elif isinstance(flag, badwing.flag.FlagYellow) and self.has_green_flag:
            success = self.has_yellow_flag = flag.collect()
        elif isinstance(flag, badwing.flag.FlagRed) and self.has_yellow_flag:
            success = self.has_red_flag = flag.collect()

        self.level_beat = self.has_red_flag

        return success