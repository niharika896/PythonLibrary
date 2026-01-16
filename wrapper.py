import copy
import json
import sys
from typing import Dict, List, Optional, Type
from ocean_lib.common.constants import Ability
from ocean_lib.models.game_state import GameState, PermanentEntities, VisibleEntities
from ocean_lib.models.entities import Algae, Bank, Bot, EnergyPad, VisibleScrap
from ocean_lib.core.strategy import BotStrategy
from ocean_lib.core.context import BotContext
from ocean_lib.core.action import Action, SpawnAction
from ocean_lib.models.point import Point

from user import MasterStrategy

class GameWrapper:
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

def _parse_bot(data: Dict) -> Bot:
    """Parse bot data from JSON."""
    return Bot(
        id=data["id"],
        owner_id=data.get("owner_id", -1),
        location=Point(**data["location"]),
        energy=data["energy"],
        scraps=data.get("scraps", 0),
        abilities=[Ability(a) for a in data.get("abilities", [])],
        algae_held=data.get("algae_held", 0)
    )


def _decode_state(raw_json: str) -> GameState:
    """Parse JSON into GameState object."""
    data = json.loads(raw_json)

    vis_cen = data.get("visible_entities", {})
    enemies = [_parse_bot(b) for b in vis_cen.get("enemies", [])]
    vis_algae = [Algae(location=Point(**a["location"])) for a in vis_cen.get("algae", [])]
    vis_scraps = [VisibleScrap(location=Point(**s["location"]), amount=s.get("amount", 1)) for s in vis_cen.get("scraps", [])]
    vis_walls = [Point(**w) for w in vis_cen.get("walls", [])]

    visible = VisibleEntities(enemies=enemies, algae=vis_algae, scraps=vis_scraps, walls=vis_walls)

    perm_cen = data.get("permanent_entities", {})
    banks = [Bank(location=Point(**b["location"]), id=b.get("id",0), deposit_occuring=b.get("deposit_occuring",0), deposit_amount=b.get("deposit_amount",0), deposit_owner=b.get("deposit_owner",0), depositticksleft=b.get("depositticksleft",0)) for b in perm_cen.get("banks", [])]
    pads = [EnergyPad(location=Point(**p["location"]), id=p.get("id",0), available=p.get("available",0), ticksleft=p.get("ticksleft",0)) for p in perm_cen.get("energypads", [])]
    perm_algae = [Algae(location=Point(**a["location"])) for a in perm_cen.get("algae", [])]

    permanent = PermanentEntities(banks=banks, energypads=pads, algae=perm_algae)
    my_bots = [_parse_bot(b) for b in data.get("bots", [])]

    return GameState(
        tick=data["tick"],
        scraps=data["scraps"],
        algae=data["algae"],
        bot_count=data["bot_count"],
        max_bots=data["max_bots"],
        width=data["width"],
        height=data["height"],
        my_bots=my_bots,
        visible_entities=visible,
        permanent_entities=permanent
    )


def main():
    """
    Pure I/O wrapper for the game.
    Reads JSON from stdin, deserializes to GameState, delegates to GameEngine.play(), writes JSON to stdout.
    """
    engine = GameWrapper(master_strategy_class=MasterStrategy)

    for line in sys.stdin:
        if line:
            # Deserialize JSON to GameState
            game_state = _decode_state(line)

            # Delegate game logic to GameEngine
            actions = engine.play(game_state)

            # Serialize and write actions to stdout
            if actions is not None:
                output = [a.to_json() for a in actions]
                print(json.dumps(output))
                sys.stdout.flush()  # Ensure it's sent immediately


if __name__ == "__main__":
    main()
