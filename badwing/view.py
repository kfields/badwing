import arcade

class View(arcade.application.View):
    def __init__(self, window=None):
        super().__init__(window)
        self.ui_manager = arcade.gui.UIManager(self.window)

    def setup(self):
        pass

    def open(self):
        self.ui_manager.purge_ui_elements()
        self.setup()

    def close(self):
        self.ui_manager.purge_ui_elements()
        self.unregister_handlers()
        # pass

    def on_draw(self):
        super().on_draw()
        self.ui_manager.on_draw()

    def on_hide_view(self):
        super().on_hide_view()
        self.unregister_handlers()

    def unregister_handlers(self):
        """
        Remove handler functions (`on_...`) from :py:attr:`arcade.Window`

        Every :py:class:`arcade.View` uses its own :py:class:`arcade.gui.UIManager`,
        this method should be called in :py:meth:`arcade.View.on_hide_view()`.
        """
        self.window.remove_handlers(
            self.ui_manager.on_draw,
            self.ui_manager.on_mouse_press,
            self.ui_manager.on_mouse_release,
            self.ui_manager.on_mouse_scroll,
            self.ui_manager.on_mouse_motion,
            self.ui_manager.on_key_press,
            self.ui_manager.on_key_release,
            self.ui_manager.on_text,
            self.ui_manager.on_text_motion,
            self.ui_manager.on_text_motion_select,
        )
