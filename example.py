import sys
from ocean_lib import Game, BotStrategy, BotContext, Ability
from ocean_lib.models.entities import Bot
from ocean_lib.templates.forager import ForagerStrategy
from ocean_lib.core.action import Action
from typing import Optional

# Define a custom strategy
class AggressiveScoot(BotStrategy):
    def act(self, ctx: BotContext) -> Optional[Action]:
        # Simple logic: Move randomly or towards enemy
        enemy = ctx.get_nearest_enemy()
        if enemy:
            return ctx.move(ctx.direction_to(enemy.location))
        return None

# Define the initial spawning coordinator
class MainCoordinatorStrategy(BotStrategy):
    def act(self, ctx: BotContext) -> Optional[Action]:
        # Example: If we have enough scraps, spawn a Forager
        if ctx.scraps >= 30: 
             return ctx.spawn(
                 capabilities=[Ability.HARVEST, Ability.SPEED], 
                 strategy=ForagerStrategy()
             )
        
        # Otherwise behave like a forager
        return ForagerStrategy().act(ctx)


class MyGame(Game):
    def __init__(self, bot_id_start: int):
        super().__init__(bot_id_start)
    
    def get_strategy_for_bot(self, bot: Bot) -> BotStrategy:
        return MainCoordinatorStrategy()

if __name__ == "__main__":
    game = MyGame(1000)
    for line in sys.stdin:
        if line:
            game.run(line)
