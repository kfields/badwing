from crunge.engine.channel import Channel

from ..screens.start_screen import StartScreen


class StartChannel(Channel):
    def produce_view(self):
        return super().produce_view()