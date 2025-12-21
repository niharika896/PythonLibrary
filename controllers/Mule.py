from .BotBase import BotController

class Mule(BotController):
    # ---- Movement ----
    def move(self, direction):
        return self.ctx.move(direction)

    # ---- Sensing ----
    def sense_scraps(self):
        return self.ctx.senseObjects()["scraps"]
