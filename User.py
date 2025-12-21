"""
USER STRATEGIES ONLY

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
from .Helper import *
from .controllers.BotBase import BotController


# ============================================================
# BOT STRATEGIES
# ============================================================

class Forager(BotController):
    def act(self):
        ctx = self.ctx
        if ctx.senseAlgae():
            return harvest(ctx.getID(), Direction.NORTH)
        return move(ctx.getID(), Direction.EAST)


class FlashScout(BotController):
    def act(self):
        return move(self.ctx.getID(), Direction.NORTH)


class Hoarder(BotController):
    def act(self):
        ctx = self.ctx
        if ctx.senseObjects()["scraps"]:
            return move(ctx.getID(), Direction.WEST)
        if ctx.senseAlgae():
            return harvest(ctx.getID(), Direction.NORTH)
        return move(ctx.getID(), Direction.EAST)


class Mule(BotController):
    def act(self):
        ctx = self.ctx
        if ctx.senseObjects()["scraps"]:
            return move(ctx.getID(), Direction.WEST)
        return move(ctx.getID(), Direction.EAST)


class Lurker(BotController):
    def act(self):
        ctx = self.ctx
        enemies = ctx.senseEnemyNearby()
        if enemies:
            e = enemies[0]
            return attack(ctx.getID(), e.location.x, e.location.y)
        return move(ctx.getID(), Direction.SOUTH)


class Saboteur(BotController):
    def act(self):
        ctx = self.ctx
        enemies = ctx.senseEnemyNearby()
        if len(enemies) > 1:
            return self_destruct(ctx.getID())
        if enemies:
            e = enemies[0]
            return attack(ctx.getID(), e.location.x, e.location.y)
        return move(ctx.getID(), Direction.WEST)


class HeatSeeker(BotController):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.target = None

    def act(self):
        ctx = self.ctx
        if self.target is None:
            enemies = ctx.senseEnemyNearby()
            if enemies:
                self.target = enemies[0].location

        if self.target:
            bx, by = ctx.getLocation().x, ctx.getLocation().y
            tx, ty = self.target.x, self.target.y

            if bx == tx and by == ty:
                return self_destruct(ctx.getID())
            if bx < tx:
                return move(ctx.getID(), Direction.EAST)
            if bx > tx:
                return move(ctx.getID(), Direction.WEST)
            if by < ty:
                return move(ctx.getID(), Direction.NORTH)
            if by > ty:
                return move(ctx.getID(), Direction.SOUTH)

        return move(ctx.getID(), Direction.NORTH)


class CustomBot(BotController):
    def act(self):
        ctx = self.ctx
        enemies = ctx.senseEnemyNearby()
        if enemies:
            e = enemies[0]
            return attack(ctx.getID(), e.location.x, e.location.y)
        if ctx.senseAlgae():
            return harvest(ctx.getID(), Direction.NORTH)
        return move(ctx.getID(), Direction.EAST)


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
            Ability.HARVEST.value,
            Ability.SCOUT.value,
        ]

        if can_afford(api, abilities):
            actions.append(spawn("Forager", abilities))

    return actions
