"""
USER STRATEGIES ONLY (PERSISTENT STRATEGY MODEL)

You define:
- Bot strategies (classes)
- Spawn decisions (inside play)

You do NOT:
- read input
- write output
- manage engine lifecycle
"""

from .API import GameAPI
from .BotContext import BotContext
from .Constants import Ability, Direction
from .Translate import *
from .controllers.BotBase import BotController
from .templates import Forager, FlashScout, HeatSeeker, Lurker, Saboteur


# ============================================================
# PERSISTENT STRATEGY REGISTRY
# ============================================================

BOT_STRATEGIES = {}   # bot_id -> strategy instance

class CustomBot(BotController):
    def act(self):
        pass
    # write the code here


# ============================================================
# TEMPLATE → STRATEGY MAP
# ============================================================

TEMPLATE_TO_STRATEGY = {
    "Forager": Forager,
    "FlashScout": FlashScout,
    "Lurker": Lurker,
    "Saboteur": HeatSeeker,
    "HeatSeeker": Saboteur,
    "CustomBot": CustomBot,
}


# ============================================================
# COST CHECK (OPTIONAL USER UTILITY)
# ============================================================

def can_afford(api: GameAPI, abilities: list[str]) -> bool:
    from .Constants import ABILITY_COSTS
    return sum(ABILITY_COSTS[a]["scrap"] for a in abilities) <= api.get_scraps()


# ============================================================
# MAIN ENTRY POINT
# ============================================================

def play(api: GameAPI):
    actions = []

    # ---------------- SPAWN PHASE ----------------
    if api.view.bot_count < api.view.max_bots:
        abilities = [
            Ability.HARVEST.value,
            Ability.SCOUT.value,
            Ability.LOCKPICK.value
        ]

        if can_afford(api, abilities):
            actions.append(spawn("Forager", abilities))
            
            
        if api.view.visible_enemies():
            for enemy in api.view.visible_enemies():
                actions.append(spawn("HeatSeeker", [Ability.SELF_DESTRUCT.value],enemy.location))

    # ---------------- EXECUTION PHASE ----------------
    for bot in api.get_my_bots():
        ctx = BotContext(api, bot)

        if bot.id not in BOT_STRATEGIES:
            strategy_cls = TEMPLATE_TO_STRATEGY.get(
                bot.template,
                CustomBot
            )
            BOT_STRATEGIES[bot.id] = strategy_cls(ctx)

        action = BOT_STRATEGIES[bot.id].act()
        if action:
            actions.append(action)

    return actions
