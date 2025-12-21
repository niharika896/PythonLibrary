from .BotBase import BotController
from ..Constants import Direction

class Hoarder(BotController):
    
    # ---- Movement ----
    def move(self, direction: Direction):
        return self.ctx.move(direction)

    # ---- Harvesting ----
    def harvest(self, direction: Direction):
        return self.ctx.harvestAlgae(direction)

    # ---- Scavenging ----
    def sense_scraps(self):
        return self.ctx.senseObjects()["scraps"]

    def sense_algae(self):
        return self.ctx.senseAlgae()
