from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player

# 1. Define the interface contract
class Collectible(Protocol):
    def on_collect(self, player: "Player") -> bool:
        ...