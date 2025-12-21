from .BotBase import BotController
from ..Constants import Direction

class Forager(BotController):

    def move(self, direction: Direction):
        return self.ctx.move(direction)

    def harvest(self, direction: Direction):
        return self.ctx.harvestAlgae(direction)

    def sense_algae(self):
        return self.ctx.senseAlgae()
