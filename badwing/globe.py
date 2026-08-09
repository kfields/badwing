from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from badwing.badwing import BadWing
    from badwing.scene import Scene
    from badwing.screens.scene_screen import SceneScreen
    from badwing.player import Player
    #from badwing.level import Level
    from badwing.characters.avatar import Avatar

app: "BadWing" = None
screen: "SceneScreen" = None
scene: "Scene" = None
player: "Player" = None
avatar: "Avatar" = None
