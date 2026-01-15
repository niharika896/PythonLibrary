from ocean_lib.common.constants import Ability
from ocean_lib.core.context import BotContext
from ocean_lib.core.strategy import BotStrategy
from ocean_lib.models.entities import Bot
from ocean_lib.models.point import Point
from ocean_lib.templates.forager import ForagerStrategy
from ocean_lib.core.action import Action
from typing import Optional
import random


# Define a custom strategy
class AggressiveScoot(BotStrategy):
    def act(self, ctx: BotContext) -> Optional[Action]:
        # Simple logic: Move towards enemy
        enemy = ctx.get_nearest_enemy()
        if enemy:
            return ctx.move(ctx.direction_to(enemy.location))
        return None

# Define the master spawning strategy
class MasterStrategy(BotStrategy):
    """
    The main strategy that controls the first bot and decision making for spawning.
    """
    def act(self, ctx: BotContext) -> Optional[Action]:
        # Example: If we have enough scraps, spawn a Forager
        if ctx.scraps >= 30:
             # Generate a random ID for the new bot or use a counter if we were persistent.
             # Since this is a simple example, we'll just pick a random int.
             # In a real game, you'd want robust ID management.
             new_id = random.randint(100, 99999) 
             
             return ctx.spawn(
                 capabilities=[Ability.HARVEST, Ability.SPEED],
                 strategy=ForagerStrategy(),
                 location=Point(0,10), # Needs better logic for valid spawn points
                 new_bot_id=new_id # Passing the ID explicitly
             )

        # Otherwise behave like a forager
        return ForagerStrategy().act(ctx)