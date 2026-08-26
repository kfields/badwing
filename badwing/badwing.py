import importlib.resources

from loguru import logger

from crunge.engine import App
from crunge.engine.resource.resource_manager import ResourceManager

from badwing import __version__
import badwing.globe
from badwing.player import Player

from .scene_screen import SceneScreen


class BadWing(App):
    display: SceneScreen
    def __init__(self, debug=False):
        super().__init__(title="BadWing")
        badwing.globe.app = self
        self.debug = debug
        self.scene = None
        self.player = Player()

    def on_display(self):
        super().on_display()
        self.scene = self.display.scene
        badwing.globe.player.level = self.scene

        gui = self.display.gui # initialize the GUI overlay

    def install(self, name):
        logger.debug(f"Installing: {name}")
        import importlib.util

        spec = importlib.util.find_spec(name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module, install = module, module.install
        install(self)

def main(debug=False, levelname="start"):
    resource_root = importlib.resources.path("badwing.resources", "")

    ResourceManager().add_path_variable("resources", resource_root)

    app = BadWing(debug=debug)
    app.install("badwing.channels.start")
    app.install("badwing.channels.playground")
    app.install("badwing.channels.cavern")
    app.install("badwing.channels.end")
    app.show_channel(levelname)
    app.run()


if __name__ == "__main__":
    main()
