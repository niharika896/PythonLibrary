from typing import Dict, List, Optional
from abc import ABC

from ..models.game_state import GameState
from ..models.entities import Bot
from ..models.point import Point
from ..common.constants import Ability
from .strategy import BotStrategy
from .context import BotContext
from .action import Action, SpawnAction

class Game(ABC):
    """
    The main game engine logic.
    Maintains persistent bot strategies.
    """

    def __init__(self, bot_id_start: int):
        self._strategies: Dict[int, BotStrategy] = {}
        self._next_bot_id = bot_id_start
        self._current_actions: List[Action] = []

    def play(self, game_state: GameState) -> List[Action]:
        """
        Processes a single tick of the game.
        Updates Strategies -> Returns Actions.
        """
        try:
            actions = self._execute_tick(game_state)
            return actions
        except Exception:
            # For resilience, returning empty list is safer for the match.
            return []

    def _execute_tick(self, game_state: GameState) -> List[Action]:
        # Reset actions for this tick
        self._current_actions = []
        
        # We'll track which bots are alive this tick to clean up old strategies
        alive_bot_ids = set()

        for bot in game_state.my_bots:
            alive_bot_ids.add(bot.id)
            
            # 1. Get or Create Strategy (if using persistence, hydration would happen here)
            strategy = self._strategies.get(bot.id)
            if not strategy:
                # If a bot exists but has no strategy (e.g. initial bot), 
                # we skip it or could assign a default. 
                # Ideally, ALL bots should have been spawned by us with a strategy, 
                # except the very first one which might need manual injection if not handled.
                continue

            # 2. Execute Strategy
            ctx = BotContext(bot, game_state)
            try:
                # Strategy.act() may return an action directly, 
                # OR it might populate ctx._pending_actions via ctx methods.
                direct_action = strategy.act(ctx)
                
                # Collect all actions (returned one + any pending ones)
                if direct_action:
                    ctx._pending_actions.append(direct_action)
                
                # Process collected actions for this bot
                for action in ctx._pending_actions:
                    
                    # Intercept SpawnActions to handle ID assignment and Strategy registration
                    if isinstance(action, SpawnAction):
                        action.new_bot_id = self._next_bot_id
                        self._next_bot_id += 1
                        # Register the strategy for the new bot
                        if action.strategy:
                            self._strategies[action.new_bot_id] = action.strategy
                    
                    self._current_actions.append(action)

            except Exception:
                # Prevent one bot's crash from killing the whole turn
                pass

        # 3. Lazy Cleanup: Remove strategies for dead bots
        # We do this after iterating to avoid modifying dict while iterating if we were iterating keys.
        # But here we iterate game_state.my_bots, so it's safe to modify self._strategies.
        # Actually, let's just do a quick pass to keep memory clean.
        existing_ids = list(self._strategies.keys())
        for bid in existing_ids:
            if bid not in alive_bot_ids:
                del self._strategies[bid]

        return self._current_actions
