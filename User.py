"""
USER STRATEGIES ONLY

You may:
- Define new bot strategy classes
- Register them in TEMPLATE_TO_STRATEGY
- Decide WHEN and WHICH bots to spawn
- Decide actions for your bots

You may NOT:
- Generate bot IDs
- Serialize output
- Access engine internals
"""

from .controllers.BotBase import BotController
from .Constants import Ability, Direction
from .models.Point import Point
from .templates import Forager, FlashScout, HeatSeeker, Lurker, Saboteur


# ============================================================
# CUSTOM BOT EXAMPLE
# ============================================================

class MinerBot(BotController):
    TEMPLATE = "MinerBot"

    def act(self):
        ctx = self.ctx

        if ctx.getAlgaeHeld() >= 5:
            bank = ctx.getNearestBank()
            d = ctx.moveTarget(ctx.getLocation(), bank)
            if d:
                return ctx.move(d)

        algae = ctx.senseAlgae()
        if algae:
            return ctx.harvestAlgae(Direction.NORTH)

        return ctx.move(Direction.NORTH)



# ============================================================
# SPAWN POLICY
# ============================================================

def spawn_policy(api):
    spawns = []

    if api.view.bot_count < api.view.max_bots:
        spawns.append(
            MinerBot.spawn(
                abilities=[
                    Ability.HARVEST.value,
                    Ability.SCOUT.value,
                ],
                location=0
            )
        )

        spawns.append(
            Forager.spawn(
                abilities=[Ability.LOCKPICK.value],
                location=2
            )
        )

    return spawns
