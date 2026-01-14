from typing import Optional
from ..core.strategy import BotStrategy
from ..core.context import BotContext
from ..core.action import Action
from ..common.constants import Direction

class FlashScoutStrategy(BotStrategy):
    """
    Moves fast (2 steps) towards algae to scout.
    """
    def act(self, ctx: BotContext) -> Optional[Action]:
        # Priority: Closest Algae
        
        # 1. Nearby check (radius 1)
        visible = ctx.get_algae_in_radius(radius=1)
        if visible:
            target_loc = visible[0].location
            return ctx.move(ctx.direction_to(target_loc), step=2)

        # 2. Expanding radius search
        radius = 2
        while radius <= 10:
            visible = ctx.get_algae_in_radius(radius)
            if visible:
                target_loc = visible[0].location
                return ctx.move(ctx.direction_to(target_loc), step=2)
            radius += 1

        return ctx.move(Direction.NORTH, step=2)
