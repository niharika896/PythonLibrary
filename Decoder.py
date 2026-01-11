import json

from .models import *


def decode_player_view(raw_json: str) -> PlayerView:
    data = json.loads(raw_json)

    enemies = [
        EnemyBot(
            id=e["id"],
            location=Point(**e["location"]),
            scraps=e["scraps"],
            abilities=e["abilities"],
        )
        for e in data["visible_entities"].get("enemies", [])
	]

    algae = [
        Algae(**a)
        for a in data["visible_entities"].get("algae", [])
	]

    scraps = [
        VisibleScrap(**s)
        for s in data["visible_entities"].get("scraps", [])
	]

    visible = VisibleEntities(enemies=enemies, algae=algae,scraps=scraps)

    banks = [Bank(**b) for b in data["permanent_entities"]["banks"]]
    pads = [EnergyPad(**p) for p in data["permanent_entities"]["energypads"]]

    permanent = PermanentEntities(banks=banks, energypads=pads)

    bots = [Bot(**b) for b in data["bots"]]

    return PlayerView(
        tick=data["tick"],
        scraps=data["scraps"],
        algae=data["algae"],
        bot_count=data["bot_count"],
        max_bots=data["max_bots"],
        width=data["width"],
        height=data["height"],
        bots=bots,
        visible_entities=visible,
        permanent_entities=permanent,
    )
