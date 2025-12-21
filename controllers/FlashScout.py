from .BotBase import BotController


class FlashScout(BotController):
    def __init__(self, ctx, move_direction):
        super().__init__(ctx)
        self.move_direction = move_direction

    def act(self):
        return self.move(self.move_direction)
