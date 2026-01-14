from typing import Optional
from ..core.strategy import BotStrategy
from ..core.wrapper import BotWrapper
from ..core.action import Action

class ForagerStrategy(BotStrategy):
    """
    A simple strategy that collects algae and dumps it at a bank.
    """
    def act(self, bot: BotWrapper) -> Optional[Action]:
        # 1. If we are full of algae, go to bank
        # Note: 'full' logic depends on carry capacity, but simple check is > 0 or specific amount
        # Original code used >= 5
        if bot.bot.algae_held >= 5:
            bank = bot.get_nearest_bank()
            if bank:
                # Move towards bank
                direction = bot.direction_to(bank.location)
                return bot.move(direction)
        
        # 2. If we see resources, harvest them
        # Check if we are ON TOP of algae or ADJACENT?
        # Helper API provided 'harvest(direction)' implying we harvest adjacent.
        # Check adjacent algae
        nearest_algae = bot.get_nearest_algae()
        if nearest_algae:
            dist = bot.location - nearest_algae.location # Point subtraction
            # Check if adjacent (manhattan distance is 1)
            if abs(dist.x) + abs(dist.y) == 1:
                direction = bot.direction_to(nearest_algae.location)
                return bot.harvest(direction)
            else:
                 # Move towards it
                direction = bot.direction_to(nearest_algae.location)
                return bot.move(direction)
        
        return None
