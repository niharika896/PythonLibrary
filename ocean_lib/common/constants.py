from enum import Enum
from typing import Dict, TypedDict

class Direction(str, Enum):
    """Cardinal directions for movement and interaction."""
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"

class Ability(str, Enum):
    """Bot abilities that determine what they can do."""
    SPEED = "SPEED"
    HARVEST = "HARVEST"
    CARRY = "CARRY"
    REPAIR = "REPAIR"
    SHIELD = "SHIELD"
    ATTACK = "ATTACK"
    SABOTAGE = "SABOTAGE"
    SELF_DESTRUCT = "SELF_DESTRUCT"
    CLOAK = "CLOAK"
    SCOUT = "SCOUT"
    LOCKPICK = "LOCKPICK"

class BotType(str, Enum):
    """Classification of bots based on ability sets."""
    SCOUT = "SCOUT"
    HARVESTER = "HARVESTER"
    TANK = "TANK"
    CLOAKER = "CLOAKER"

class ActionType(str, Enum):
    """Types of actions a bot can perform."""
    MOVE = "MOVE"
    HARVEST = "HARVEST"
    ATTACK = "ATTACK"
    REPAIR = "REPAIR"
    SELF_DESTRUCT = "SELF_DESTRUCT"
    SPAWN = "SPAWN"

class AbilityCost(TypedDict):
    scrap: int
    energy: float

ABILITY_COSTS: Dict[str, AbilityCost] = {
    "SPEED": {"scrap": 5, "energy": 2.0},
    "HARVEST": {"scrap": 5, "energy": 1.0},
    "CARRY": {"scrap": 5, "energy": 0.5},
    "REPAIR": {"scrap": 10, "energy": 3.0},
    "SHIELD": {"scrap": 10, "energy": 1.0},
    "ATTACK": {"scrap": 15, "energy": 4.0},
    "SABOTAGE": {"scrap": 20, "energy": 5.0},
    "SELF_DESTRUCT": {"scrap": 5, "energy": 50.0},
    "CLOAK": {"scrap": 25, "energy": 5.0},
    "SCOUT": {"scrap": 5, "energy": 1.0},
    "LOCKPICK": {"scrap": 10, "energy": 0.0},
}
