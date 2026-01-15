from ocean_lib.common.constants import Ability
from ocean_lib.core.context import BotContext
from ocean_lib.core.game import Game
from ocean_lib.core.strategy import BotStrategy
from ocean_lib.models.entities import Bot
from ocean_lib.models.point import Point
from ocean_lib.templates.forager import ForagerStrategy
from ocean_lib.core.action import Action
from typing import Optional


# Define a custom strategy
class AggressiveScoot(BotStrategy):
    def act(self, ctx: BotContext) -> Optional[Action]:
        # Simple logic: Move towards enemy
        enemy = ctx.get_nearest_enemy()
        if enemy:
            return ctx.move(ctx.direction_to(enemy.location))
        return None

# Define the initial spawning coordinator
class MainCoordinatorStrategy(BotStrategy):
    def act(self, ctx: BotContext) -> Optional[Action]:
        # Example: If we have enough scraps, spawn a Forager
        if ctx.scraps >= 30:
             ctx.spawn(
                 capabilities=[Ability.HARVEST, Ability.SPEED],
                 strategy=ForagerStrategy(),
                 location=Point(0,10)
             )
             return None  # spawn already appended to actions

        # Otherwise behave like a forager
        return ForagerStrategy().act(ctx)


class MyGame(Game):
    pass
