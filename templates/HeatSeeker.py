from ..controllers.BotBase import BotController
from ..Translate import *
from ..Constants import Direction

class HeatSeeker(BotController):
    def __init__(self, ctx, target):
        super().__init__(ctx)
        self.target = target

    def act(self):
        ctx = self.ctx
        bot_pos = ctx.getLocation()

        if bot_pos.x == self.target.x and bot_pos.y == self.target.y:
            return self_destruct(ctx.getID())

        d = ctx.moveTarget(bot_pos, self.target)
        if d:
            return move(ctx.getID(), d)
        
        return None
