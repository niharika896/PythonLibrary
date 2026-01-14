from typing import Optional
from ..core.strategy import BotStrategy
from ..core.wrapper import BotWrapper
from ..core.action import Action
from ..common.constants import Direction

class FlashScoutStrategy(BotStrategy):
    """
    Moves fast (2 steps) towards algae to scout.
    """
    def act(self, bot: BotWrapper) -> Optional[Action]:
        # Priority: Closest Algae
        
        # 1. Nearby check (radius 1)
        # Note: If we use speed, we can move 2 steps!
        visible = bot.get_algae_in_radius(radius=1)
        if visible:
            target_loc = visible[0].location
            return bot.move(bot.direction_to(target_loc), step=2)

        # 2. Expanding radius search
        radius = 2
        while radius <= 10:
            visible = bot.get_algae_in_radius(radius)
            if visible:
                target_loc = visible[0].location
                return bot.move(bot.direction_to(target_loc), step=2)
            radius += 1

        return bot.move(Direction.NORTH, step=2)
