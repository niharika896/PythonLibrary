import copy
from typing import Dict, List, Optional, Type
from ocean_lib.models.game_state import GameState
from ocean_lib.models.entities import Bot
from ocean_lib.core.strategy import BotStrategy
from ocean_lib.core.context import BotContext
from ocean_lib.core.action import Action, SpawnAction

class GameEngine:
    """
    The main game engine logic.
    Maintains persistent bot strategies and maps bot IDs to their strategies.
    """

    def __init__(self, master_strategy_class: Type[BotStrategy]):
        self._strategies: Dict[int, BotStrategy] = {}
        self._master_strategy_class = master_strategy_class

    def play(self, game_state: GameState) -> List[Action]:
        """
        Processes a single tick of the game.
        """
        try:
            actions = self._execute_tick(game_state)
            return actions
        except Exception:
            return []

    def _execute_tick(self, game_state: GameState) -> List[Action]:
        current_actions = []
        alive_bot_ids = set()

        for bot in game_state.my_bots:
            alive_bot_ids.add(bot.id)
            
            # 1. Get or Create Strategy
            strategy = self._strategies.get(bot.id)
            if not strategy:
                # If it's the very first bot (no owner or similar heuristic might be needed if IDs aren't sequential)
                # For now, we assume if we don't have a strategy for a bot, and it's alive,
                # it might be the initial bot spawned by the system using the Master Strategy.
                # In a real scenario, we might want to be more specific (e.g. check if it's bot 0).
                # But for now, if a bot shows up and we don't know it, we give it the Master Strategy.
                # This logic replaces the explicit "MyGame" initialization.
                strategy = self._master_strategy_class()
                self._strategies[bot.id] = strategy

            # 2. Execute Strategy
            ctx = BotContext(bot, game_state)
            try:
                direct_action = strategy.act(ctx)
                
                if direct_action:
                    current_actions.append(direct_action)

            except Exception:
                pass

        # 3. Cleanup dead strategies
        existing_ids = list(self._strategies.keys())
        for bid in existing_ids:
            if bid not in alive_bot_ids:
                del self._strategies[bid]

        return current_actions
