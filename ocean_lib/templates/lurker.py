from typing import Optional
from ..core.strategy import BotStrategy
from ..core.wrapper import BotWrapper
from ..core.action import Action
from ..common.constants import Direction

class LurkerStrategy(BotStrategy):
    """
    Stand still and attack any enemy that comes close.
    Patrols South if no enemy.
    """
    def act(self, bot: BotWrapper) -> Optional[Action]:
        # Sense nearby enemies
        enemies = bot.get_visible_enemies()
        # Old template picked the first one available in the list
        
        if enemies:
            e = enemies[0]
            return bot.attack(e.location)
            
        return bot.move(Direction.SOUTH)
