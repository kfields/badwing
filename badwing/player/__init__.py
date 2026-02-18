import badwing.globe
import badwing.objects.coin
import badwing.characters.butterfly
import badwing.objects.flag


class LevelProgress:
    def __init__(self, level_id):
        self.level_id = level_id
        self.score_achieved = 0
        self.has_green_flag = False
        self.has_yellow_flag = False
        self.has_red_flag = False
        self.is_completed = False

    def restart(self):
        self.score_achieved = 0
        self.has_green_flag = False
        self.has_yellow_flag = False
        self.has_red_flag = False
        self.is_completed = False

    def check_completion(self):
        if self.has_red_flag:
            self.is_completed = True
        return self.is_completed


class Player:
    def __init__(self):
        badwing.globe.player = self
        self.score = 0
        self.level_progress: LevelProgress = None
        self.progress_history: dict[str, LevelProgress] = {}
        self.on_next_level()

    def add_level_progress(self, level_progress: LevelProgress):
        self.progress_history[level_progress.level_id] = level_progress

    def restart_level(self):
        self.level_progress.restart()

    def on_next_level(self):
        self.level_progress = LevelProgress("level1")
    """
    def on_next_level(self):
        self.has_green_flag = False
        self.has_yellow_flag = False
        self.has_red_flag = False
        self.level_beat = False
    """

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
        self.score += 1
        return True

    def collect_butterfly(self, item):
        self.score += 1
        return True

    def collect_flag(self, flag):
        success = False
        if isinstance(flag, badwing.objects.flag.FlagGreen) and not self.level_progress.has_green_flag:
            success = self.level_progress.has_green_flag = flag.collect()
        elif isinstance(flag, badwing.objects.flag.FlagYellow) and self.level_progress.has_green_flag:
            success = self.level_progress.has_yellow_flag = flag.collect()
        elif isinstance(flag, badwing.objects.flag.FlagRed) and self.level_progress.has_yellow_flag:
            success = self.level_progress.has_red_flag = flag.collect()

        self.level_progress.is_completed = self.level_progress.has_red_flag

        return success
