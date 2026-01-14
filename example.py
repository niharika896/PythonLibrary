import sys
from ocean_lib import Game, BotStrategy, BotWrapper, Point, Ability
from ocean_lib.models.entities import Bot
from ocean_lib.templates.forager import ForagerStrategy
from ocean_lib.core.action import Action
from typing import Optional

# Define a custom strategy
class AggressiveScoot(BotStrategy):
    def act(self, bot: BotWrapper) -> Optional[Action]:
        # Simple logic: Move randomly or towards enemy
        enemy = bot.get_nearest_enemy()
        if enemy:
            return bot.move(bot.direction_to(enemy.location))
        return None

# Define the initial spawning coordinator
class MainCoordinatorStrategy(BotStrategy):
    """
    The initial bot (if any) or a virtual strategy can be used to manage spawns.
    Wait, in this game do we start with a bot? Or do we act as a 'God' initially?
    Usually we start with 1 bot.
    """
    def act(self, bot: BotWrapper) -> Optional[Action]:
        # Example: If we have enough scraps, spawn a Forager
        if bot.scraps >= 30: # Assuming cost
             # Using the NEW spawn API: Pass the strategy INSTANCE
             return bot.spawn(
                 abilities=[Ability.HARVEST, Ability.SPEED], 
                 strategy=ForagerStrategy()
             )
        
        # Otherwise behave like a forager
        return ForagerStrategy().act(bot)


class MyGame(Game):
    def __init__(self, bot_id_start: int):
        super().__init__(bot_id_start)
    
    def get_strategy_for_bot(self, bot: Bot) -> BotStrategy:
        # This is the FALLBACK for the initial bots (that exist at tick 0 before we spawn anything)
        # or if the queue is empty.
        
        # E.g. The first bot is our "Coordinator"
        return MainCoordinatorStrategy()

if __name__ == "__main__":
    game = MyGame(1000)
    for line in sys.stdin:
        if line:
            game.run(line)
