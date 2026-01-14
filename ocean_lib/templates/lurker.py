from typing import Optional
from ..core.strategy import BotStrategy
from ..core.context import BotContext
from ..core.action import Action
from ..common.constants import Direction

class LurkerStrategy(BotStrategy):
    """
    Stand still and attack any enemy that comes close.
    Patrols South if no enemy.
    """
    def act(self, ctx: BotContext) -> Optional[Action]:
        enemies = ctx.get_visible_enemies()
        
        if enemies:
            e = enemies[0]
            return ctx.attack(e.location)
            
        return ctx.move(Direction.SOUTH)
