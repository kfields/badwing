import badwing.globe
import badwing.objects.coin
import badwing.characters.butterfly
import badwing.objects.flag

class Player:
    def __init__(self):
        badwing.globe.player = self
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
        if isinstance(item, badwing.objects.coin.Coin):
            return self.collect_coin(item)
        if isinstance(item, badwing.characters.butterfly.Butterfly):
            return self.collect_butterfly(item)
        elif isinstance(item, badwing.objects.flag.Flag):
            return self.collect_flag(item)

    def collect_coin(self, item):
        self.score +=1
        return True

    def collect_butterfly(self, item):
        self.score +=1
        return True

    def collect_flag(self, flag):
        success = False
        if isinstance(flag, badwing.objects.flag.FlagGreen) and not self.has_green_flag:
            success = self.has_green_flag = flag.collect()
        elif isinstance(flag, badwing.objects.flag.FlagYellow) and self.has_green_flag:
            success = self.has_yellow_flag = flag.collect()
        elif isinstance(flag, badwing.objects.flag.FlagRed) and self.has_yellow_flag:
            success = self.has_red_flag = flag.collect()

        self.level_beat = self.has_red_flag

        return success