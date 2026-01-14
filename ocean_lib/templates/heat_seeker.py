from typing import Optional
from ..core.strategy import BotStrategy
from ..core.context import BotContext
from ..core.action import Action
from ..models.point import Point

class HeatSeekerStrategy(BotStrategy):
    """
    Moves to a specific static target and self-destructs.
    """
    def __init__(self, target: Point):
        self.target = target

    def act(self, ctx: BotContext) -> Optional[Action]:
        if ctx.location == self.target:
            return ctx.self_destruct()

        direction = ctx.direction_to(self.target)
        return ctx.move(direction)
