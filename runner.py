import sys
import json
from typing import Dict

from ocean_lib.models.game_state import GameState, VisibleEntities, PermanentEntities
from ocean_lib.models.entities import Bot, Algae, VisibleScrap, Bank, EnergyPad
from ocean_lib.models.point import Point
from ocean_lib.common.constants import Ability


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


def run(game):
    """
    Pure I/O wrapper for the game.
    Reads JSON from stdin, deserializes to GameState, delegates to Game.play(), writes JSON to stdout.
    """
    for line in sys.stdin:
        if line:
            # Deserialize JSON to GameState
            game_state = _decode_state(line)
            
            # Delegate game logic to Game
            actions = game.play(game_state)

            # Serialize and write actions to stdout
            if actions is not None:
                output = [a.to_json() for a in actions]
                print(json.dumps(output))
                sys.stdout.flush()  # Ensure it's sent immediately


if __name__ == "__main__":
    from user import MyGame
    game = MyGame(bot_id_start=0)
    run(game)