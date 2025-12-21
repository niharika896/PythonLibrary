from .BotBase import BotController

class Saboteur(BotController):
    # ---- Sensing ----
    def sense_enemies(self):
        return self.ctx.senseEnemyNearby()

    # ---- Combat ----
    def attack(self, location):
        return self.ctx.attack(location)

    def self_destruct(self):
        return self.ctx.selfDestruct()

    # ---- Movement ----
    def move(self, direction):
        return self.ctx.move(direction)
