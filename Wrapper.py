"""
ENGINE WRAPPER

Handles:
- Bot ID allocation
- Strategy persistence
- Context rebinding
- Cleanup of dead bots
- Engine contract compliance
"""

from .API import GameAPI
from .BotContext import BotContext
from .Translate import spawn
from .controllers.BotBase import BotController
from .templates import Forager, FlashScout, HeatSeeker, Lurker, Saboteur
from .User import TEMPLATE_TO_STRATEGY as USER_TEMPLATE_TO_STRATEGY, spawn_policy


# ============================================================
# STRATEGY REGISTRY (PERSISTENT)
# ============================================================

BOT_STRATEGIES: dict[int, BotController] = {}


# ============================================================
# TEMPLATE → STRATEGY MAP
# (Engine defaults + user overrides)
# ============================================================


# ============================================================
# ENGINE ENTRY POINT
# ============================================================

def play(api: GameAPI):
    """
    Called once per tick by the engine.

    Returns:
        {
            "spawn": { bot_id: spawn_payload },
            "actions": { bot_id: action_payload }
        }
    """

    spawns: dict[str, dict] = {}
    actions: dict[str, dict] = {}

    # ---------------- SPAWN PHASE ----------------
    for spec in spawn_policy(api):
        strategy_cls = spec["strategy"]

        bot_id, payload = spawn(
            abilities=spec["abilities"],
            location=spec["location"]
        )

        spawns[str(bot_id)] = payload

        # Bind strategy instance
        BOT_STRATEGIES[bot_id] = strategy_cls(None)


    # ---------------- EXECUTION PHASE ----------------
    alive_ids = set()

    for bot in api.get_my_bots():
        alive_ids.add(bot.id)
        ctx = BotContext(api, bot)

        if bot.id not in BOT_STRATEGIES:
            strategy_cls = TEMPLATE_TO_STRATEGY.get(bot.template)
            if strategy_cls is None:
                raise ValueError(f"Unknown bot template: {bot.template}")

            BOT_STRATEGIES[bot.id] = strategy_cls(ctx)

        # Rebind context every tick
        BOT_STRATEGIES[bot.id].ctx = ctx

        action = BOT_STRATEGIES[bot.id].act()
        if action:
            actions[str(bot.id)] = action.to_dict()

    # ---------------- CLEANUP ----------------
    for bid in list(BOT_STRATEGIES.keys()):
        if bid not in alive_ids:
            del BOT_STRATEGIES[bid]

    return {
        "spawn": spawns,
        "actions": actions,
    }
