from abc import ABC, abstractmethod
from typing import Optional
from .action import Action
from .wrapper import BotWrapper

class BotStrategy(ABC):
    """
    Abstract base class for all bot strategies.
    Implement the `act` method to define bot behavior.
    """

    @abstractmethod
    def act(self, bot: BotWrapper) -> Optional[Action]:
        """
        Called every tick for the bot.
        
        Args:
            bot: The BotWrapper instance providing context and actions.
            
        Returns:
            An Action to perform, or None to do nothing.
        """
        pass
