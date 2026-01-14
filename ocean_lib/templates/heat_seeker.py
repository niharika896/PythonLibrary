from typing import Optional
from ..core.strategy import BotStrategy
from ..core.wrapper import BotWrapper
from ..core.action import Action
from ..models.point import Point

class HeatSeekerStrategy(BotStrategy):
    """
    Moves to a specific static target and self-destructs.
    """
    def __init__(self, target: Point):
        self.target = target

    def act(self, bot: BotWrapper) -> Optional[Action]:
        if bot.location == self.target:
            return bot.self_destruct()

        direction = bot.direction_to(self.target)
        return bot.move(direction)
