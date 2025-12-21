"""
USER BOILERPLATE

RULES:
- Each bot class defines its own strategy
- Strategy is fixed for the bot's lifetime
- Abilities are assigned ONLY at spawn
- No upgrades
- User never controls bots after spawn
"""

from .API import GameAPI
from .BotContext import BotContext
from .Constants import Ability, Direction
from .Helper import *
from .controllers.BotBase import BotController


# ============================================================
# BOT STRATEGIES
# ============================================================

class Forager(BotController):
    def act(self):
        pass


class FlashScout(BotController):
    def act(self):
        pass


class Hoarder(BotController):
    def act(self):
        pass


class Mule(BotController):
    def act(self):
        pass


class Lurker(BotController):
    def act(self):
        pass

class Saboteur(BotController):
    def act(self):
        pass


class HeatSeeker(BotController):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.target = None

    def act(self):
        pass


class CustomBot(BotController):
    def act(self):
        pass


# ============================================================
# COST CHECK (OPTIONAL USER UTILITY)
# ============================================================

def can_afford(api: GameAPI, abilities: list[str]) -> bool:
    from .Constants import ABILITY_COSTS
    return sum(ABILITY_COSTS[a]["scrap"] for a in abilities) <= api.get_scraps()


# ============================================================
# SPAWN DECISIONS
# ============================================================

def play(api: GameAPI):
    actions = []

    if api.view.bot_count < api.view.max_bots:
        abilities = [
            # Ability.HARVEST.value,
            # Ability.SCOUT.value,
        ]

        if can_afford(api, abilities):
            # actions.append(spawn("Forager", abilities))

    return actions
