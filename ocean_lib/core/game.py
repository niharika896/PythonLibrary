import json
import random
from typing import Dict, List, Optional
from abc import ABC

from ..models.game_state import GameState, VisibleEntities, PermanentEntities
from ..models.entities import Bot, Algae, VisibleScrap, Bank, EnergyPad
from ..models.point import Point
from ..common.constants import Ability
from .strategy import BotStrategy
from .context import BotContext
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
        
        # Immediate mapping!
        self._strategies[new_id] = strategy
        
        return SpawnAction(abilities=capabilities, new_bot_id=new_id, spawn_location=location)

    def run(self, raw_json: str):
        try:
            game_state = self._decode_state(raw_json)
            actions = self._execute_tick(game_state)
            self._flush_actions(actions)
        except Exception:
            # Fallback
            pass

    def _execute_tick(self, game_state: GameState) -> List[Action]:
        actions = []
        current_bot_ids = set()

        # 1. Update Strategies / Bot List
        for bot in game_state.my_bots:
            current_bot_ids.add(bot.id)
            if bot.id not in self._strategies:
                self._strategies[bot.id] = self.get_strategy_for_bot(bot)

        # 2. Cleanup died bots
        existing_ids = list(self._strategies.keys())
        for bid in existing_ids:
            if bid not in current_bot_ids:
                del self._strategies[bid]

        # 3. Execute Strategies
        for bot in game_state.my_bots:
            strategy = self._strategies.get(bot.id)
            if strategy:
                ctx = BotContext(bot, game_state)
                ctx.game = self 
                try:
                    action = strategy.act(ctx)
                    if action:
                        actions.append(action)
                except Exception:
                    pass

        return actions
    
    def get_strategy_for_bot(self, bot: Bot) -> BotStrategy:
        """
        Fallback for bots not spawned via 'spawn()'.
        """
        from ..templates.forager import ForagerStrategy
        return ForagerStrategy() 

    def _flush_actions(self, actions: List[Action]):
        output = [a.to_json() for a in actions]
        print(json.dumps(output))

    def _decode_state(self, raw_json: str) -> GameState:
        data = json.loads(raw_json)
        
        vis_cen = data.get("visible_entities", {})
        enemies = [self._parse_bot(b) for b in vis_cen.get("enemies", [])]
        vis_algae = [Algae(location=Point(**a["location"])) for a in vis_cen.get("algae", [])]
        vis_scraps = [VisibleScrap(location=Point(**s["location"]), amount=s.get("amount", 1)) for s in vis_cen.get("scraps", [])]
        vis_walls = [Point(**w) for w in vis_cen.get("walls", [])]
        
        visible = VisibleEntities(enemies=enemies, algae=vis_algae, scraps=vis_scraps, walls=vis_walls)

        perm_cen = data.get("permanent_entities", {})
        banks = [Bank(location=Point(**b["location"]), id=b.get("id",0), deposit_occuring=b.get("deposit_occuring",0), deposit_amount=b.get("deposit_amount",0), deposit_owner=b.get("deposit_owner",0), depositticksleft=b.get("depositticksleft",0)) for b in perm_cen.get("banks", [])]
        pads = [EnergyPad(location=Point(**p["location"]), id=p.get("id",0), available=p.get("available",0), ticksleft=p.get("ticksleft",0)) for p in perm_cen.get("energypads", [])]
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
