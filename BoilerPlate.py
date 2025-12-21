"""
USER BOILERPLATE (PERSISTENT STRATEGY MODEL)

RULES:
- One strategy per bot (template-based)
- Strategy persists for bot lifetime
- Abilities chosen ONLY at spawn
- No upgrades
- No micromanagement
"""

from .API import GameAPI
from .BotContext import BotContext
from .Constants import Ability, Direction
from .Helper import *
from .controllers.BotBase import BotController

BOT_STRATEGIES = {}


# ---------------- BOT STRATEGIES ----------------

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


TEMPLATE_TO_STRATEGY = {
    "Forager": Forager,
    "FlashScout": FlashScout,
    "Hoarder": Hoarder,
    "Mule": Mule,
    "Lurker": Lurker,
    "Saboteur": Saboteur,
    "HeatSeeker": HeatSeeker,
    "CustomBot": CustomBot,
}


def can_afford(api: GameAPI, abilities: list[str]) -> bool:
    from .Constants import ABILITY_COSTS
    return sum(ABILITY_COSTS[a]["scrap"] for a in abilities) <= api.get_scraps()


def play(api: GameAPI):
    actions = []
    
    #Spawn bots with desired abilities (if any)

    for bot in api.get_my_bots():
        ctx = BotContext(api, bot)

        if bot.id not in BOT_STRATEGIES:
            BOT_STRATEGIES[bot.id] = TEMPLATE_TO_STRATEGY[bot.template](ctx)

        action = BOT_STRATEGIES[bot.id].act()
        if action:
            actions.append(action)

    return actions
