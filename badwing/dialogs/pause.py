import badwing.globe
import badwing.level_controller
import badwing.dialog


class Controller(badwing.level_controller.LevelController):
    def on_key_press(self, key, modifiers):
        pass


class PauseDialog(badwing.dialog.Dialog):
    def __init__(self):
        super().__init__("pause")
        self.width = badwing.globe.game.width
        self.height = badwing.globe.game.height
        self.half_width = self.width / 2
        self.half_height = self.height / 2
        self.center_x = self.width / 2
        self.center_y = self.height / 2

    def add_buttons(self):
        width = 200
        height = 50
        resume_button = gui.UIFlatButton(0, 0, width, height, "Resume")

        @resume_button.event("on_click")
        def submit(x):
            badwing.globe.scene.close_dialog()

        quit_button = gui.UIFlatButton(0, 0, width, height, "Quit")

        @quit_button.event("on_click")
        def submit(x):
            self.close()
            import badwing.scenes.start

            badwing.app.game.show_scene(badwing.scenes.start.StartScene)

        self.ui_manager.add(
            gui.UIAnchorLayout(
                children=[
                    gui.UIBoxLayout(
                        children=[resume_button, quit_button], space_between=20
                    )
                ]
            )
        )

    def _create(self):
        super()._create()
        self.add_buttons()

    def draw(self):
        super().draw()
        arcade.draw_text(
            "BadWing",
            self.center_x,
            self.center_y + 100,
            arcade.color.WHITE,
            60,
            font_name="Verdana",
        )
