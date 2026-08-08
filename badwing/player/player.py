from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from badwing.level import Level

import badwing.globe

from badwing.collectible import Collectible


class LevelProgress:
    def __init__(self, level_id, stage_count=3):
        self.level_id = level_id
        self.score = 0
        self.stage = 0
        self.stage_count = stage_count

    @property
    def is_completed(self):
        return self.stage >= self.stage_count


class Player:
    def __init__(self):
        badwing.globe.player = self
        self.score = 0
        self._level: "Level" = None
        self.level_progress: LevelProgress = None
        self.progress_history: dict[str, LevelProgress] = {}

    @property
    def level(self) -> "Level":
        return self._level

    @level.setter
    def level(self, value: "Level"):
        self._level = value
        if not value.name in self.progress_history:
            self.level_progress = value.create_progress()
            self.add_level_progress(self.level_progress)

    def add_level_progress(self, level_progress: LevelProgress):
        self.progress_history[level_progress.level_id] = level_progress

    def remove_level_progress(self, level_id: str):
        if level_id in self.progress_history:
            del self.progress_history[level_id]

    def collect(self, item: Collectible) -> bool:
        return item.on_collect(self)
