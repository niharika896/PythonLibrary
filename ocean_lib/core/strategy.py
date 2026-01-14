from abc import ABC, abstractmethod
from typing import Optional
from .action import Action
from .context import BotContext

class BotStrategy(ABC):
    """
    Abstract base class for all bot strategies.
    Implement the `act` method to define bot behavior.
    """

    @abstractmethod
    def act(self, ctx: BotContext) -> Optional[Action]:
        """
        Called every tick for the bot.
        
        Args:
            ctx: The BotContext instance providing data and actions.
            
        Returns:
            An Action to perform, or None to do nothing.
        """
        pass
