from typing import Optional
from ..core.strategy import BotStrategy
from ..core.context import BotContext
from ..core.action import Action

class ForagerStrategy(BotStrategy):
    """
    A simple strategy that collects algae and dumps it at a bank.
    """
    def act(self, ctx: BotContext) -> Optional[Action]:
        # 1. If we are full of algae, go to bank
        if ctx.bot.algae_held >= 5:
            bank = ctx.get_nearest_bank()
            if bank:
                # Move towards bank
                direction = ctx.direction_to(bank.location)
                return ctx.move(direction)
        
        # 2. If we see resources, harvest them
        nearest_algae = ctx.get_nearest_algae()
        if nearest_algae:
            dist = ctx.location - nearest_algae.location 
            if abs(dist.x) + abs(dist.y) == 1:
                direction = ctx.direction_to(nearest_algae.location)
                return ctx.harvest(direction)
            else:
                direction = ctx.direction_to(nearest_algae.location)
                return ctx.move(direction)
        
        return None
