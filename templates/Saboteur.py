from ..controllers.BotBase import BotController
from ..Translate import *
from ..Constants import Direction

class Saboteur(BotController):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.target = None   # persistent memory

    def act(self):
        ctx = self.ctx
        bot_pos = ctx.getLocation()

        close_enemies = ctx.senseEnemyinRadius(bot_pos, radius=1)
        if close_enemies:
            return self_destruct(ctx.getID())

        if self.target is None:
            radius = 2
            while radius <= 10:
                enemies = ctx.senseEnemyinRadius(bot_pos, radius)
                if enemies:
                    self.target = enemies[0].location
                    break
                radius += 1

        if self.target:
            d = ctx.moveTarget(bot_pos, self.target)
            if d:
                return move(ctx.getID(), d)
            else:
                self.target = None
                
        return move(ctx.getID(), Direction.NORTH)
