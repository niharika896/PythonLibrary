from .BotBase import BotController

class Lurker(BotController):
    # ---- Sensing ----
    def sense_enemies(self):
        return self.ctx.senseEnemyNearby()

    # ---- Combat ----
    def attack(self, location):
        return self.ctx.attack(location)

    # ---- Movement ----
    def move(self, direction):
        return self.ctx.move(direction)
