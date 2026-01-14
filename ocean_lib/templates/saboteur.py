from typing import Optional
from ..core.strategy import BotStrategy
from ..core.wrapper import BotWrapper
from ..core.action import Action
from ..models.point import Point
from ..common.constants import Direction

class SaboteurStrategy(BotStrategy):
    """
    Scans for enemies, moves towards them, and self-destructs when close.
    """
    def __init__(self):
        self.target: Optional[Point] = None

    def act(self, bot: BotWrapper) -> Optional[Action]:
        # 1. Check for close enemies (radius 1)
        close_enemies = bot.get_enemies_in_radius(radius=1)
        if close_enemies:
            return bot.self_destruct()

        # 2. Logic to find a target if we don't have one
        if self.target is None:
            radius = 2
            while radius <= 10:
                enemies = bot.get_enemies_in_radius(radius)
                if enemies:
                    self.target = enemies[0].location
                    break
                radius += 1

        # 3. Move towards target
        if self.target:
            # Check if we reached it
            if bot.location == self.target:
                self.target = None # Arrived, scan again next tick
            else:
                return bot.move(bot.direction_to(self.target))

        return bot.move(Direction.NORTH)
