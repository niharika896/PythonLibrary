import json
import random
from typing import Dict, List, Optional
from abc import ABC

from ..models.game_state import GameState, VisibleEntities, PermanentEntities
from ..models.entities import Bot, Algae, VisibleScrap, Bank, EnergyPad
from ..models.point import Point
from ..common.constants import Ability
from .strategy import BotStrategy
from .wrapper import BotWrapper
from .action import Action, SpawnAction

class Game(ABC):
    """
    The main game engine logic.
    Maintains persistent bot strategies using client-side ID generation.
    """

    def __init__(self, bot_id_start: int):
        self._strategies: Dict[int, BotStrategy] = {}
        self._next_bot_id = bot_id_start

    def spawn(self, capabilities: List[Ability], strategy: BotStrategy, location: Optional[Point] = None) -> SpawnAction:
        """
        Request to spawn a new bot. Generates an ID immediately and maps the strategy.
        """
        new_id = self._next_bot_id
        self._next_bot_id += 1
        
        # Immediate mapping! No queue needed.
        self._strategies[new_id] = strategy
        
        return SpawnAction(abilities=capabilities, new_bot_id=new_id, spawn_location=location)

    def run(self, raw_json: str):
        try:
            game_state = self._decode_state(raw_json)
            actions = self._execute_tick(game_state)
            self._flush_actions(actions)
        except Exception:
            pass

    def _execute_tick(self, game_state: GameState) -> List[Action]:
        actions = []
        current_bot_ids = set()

        # 1. Update Strategies / Bot List
        for bot in game_state.my_bots:
            current_bot_ids.add(bot.id)
            if bot.id not in self._strategies:
                # This happens if:
                # a) It's the initial bot (didn't spawn it via this library this run)
                # b) The engine ignored our ID and gave a different one (Mapping failed)
                self._strategies[bot.id] = self.get_strategy_for_bot(bot)

        # 2. Cleanup died bots
        existing_ids = list(self._strategies.keys())
        for bid in existing_ids:
            if bid not in current_bot_ids:
                # Important: Don't delete if we JUST spawned it this tick and it hasn't appeared yet!
                # But 'run' is called on tick N state.
                # If we spawed at tick N-1, it should be in tick N state.
                # If we spawn at tick N (now), it won't be in tick N state, but in our strategies map.
                # So we must NOT delete IDs that are not in current_state BUT were just created?
                # Actually, standard logic: 
                # Decode state -> process -> flush actions.
                # The strategies map contains IDs from previous ticks + newly created ones from THIS tick's logic... wait.
                # If we spawn INSIDE process(), we add to map.
                # But here we are cleaning BEFORE process().
                # So if we spawned last tick, it SHOULD be in game_state.my_bots now.
                # If it's not, it died or failed to spawn. Safe to delete?
                # Maybe wait one tick? 
                
                # To be strict: Only delete if we are sure it existed before. 
                # But simplistic cleanup is okay for now.
                del self._strategies[bid]

        # 3. Execute Strategies
        for bot in game_state.my_bots:
            strategy = self._strategies.get(bot.id)
            if strategy:
                wrapper = BotWrapper(bot, game_state)
                wrapper.game = self 
                try:
                    action = strategy.act(wrapper)
                    if action:
                        actions.append(action)
                except Exception:
                    pass

        return actions
    
    def get_strategy_for_bot(self, bot: Bot) -> BotStrategy:
        """
        Fallback for bots not spawned via 'spawn()' (e.g. initial bots).
        """
        # Default implementation, user overrides
        from ..templates.forager import ForagerStrategy
        return ForagerStrategy() 

    def _flush_actions(self, actions: List[Action]):
        output = [a.to_json() for a in actions]
        print(json.dumps(output))

    def _decode_state(self, raw_json: str) -> GameState:
        # Passthrough to previous implementation logic...
        # For brevity, I'll copy the body from previous step since I am overwriting the file.
        data = json.loads(raw_json)
        
        vis_cen = data.get("visible_entities", {})
        enemies = [self._parse_bot(b) for b in vis_cen.get("enemies", [])]
        vis_algae = [Algae(location=Point(**a["location"])) for a in vis_cen.get("algae", [])]
        vis_scraps = [VisibleScrap(location=Point(**s["location"]), amount=s.get("amount", 1)) for s in vis_cen.get("scraps", [])]
        vis_walls = [Point(**w) for w in vis_cen.get("walls", [])]
        
        visible = VisibleEntities(enemies=enemies, algae=vis_algae, scraps=vis_scraps, walls=vis_walls)

        perm_cen = data.get("permanent_entities", {})
        banks = [Bank(location=Point(**b["location"]), owner_id=b["owner_id"]) for b in perm_cen.get("banks", [])]
        pads = [EnergyPad(location=Point(**p["location"])) for p in perm_cen.get("energypads", [])]
        perm_algae = [Algae(location=Point(**a["location"])) for a in perm_cen.get("algae", [])]

        permanent = PermanentEntities(banks=banks, energypads=pads, algae=perm_algae)
        my_bots = [self._parse_bot(b) for b in data.get("bots", [])]

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

    def _parse_bot(self, data: Dict) -> Bot:
        return Bot(
            id=data["id"],
            owner_id=data.get("owner_id", -1),
            location=Point(**data["location"]),
            energy=data["energy"],
            scraps=data.get("scraps", 0),
            abilities=[Ability(a) for a in data.get("abilities", [])],
            algae_held=data.get("algae_held", 0)
        )
