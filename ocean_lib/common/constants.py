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
    HARVEST = "HARVEST"
    SCOUT = "SCOUT"
    SELF_DESTRUCT = "SELF_DESTRUCT"
    SPEED = "SPEED"
    SHIELD = "SHIELD"
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

ABILITY_COSTS: Dict[Ability, AbilityCost] = {
    Ability.HARVEST: {"scrap": 5, "energy": 1.0},
    Ability.SCOUT: {"scrap": 5, "energy": 1.0},
    Ability.SELF_DESTRUCT: {"scrap": 5, "energy": 50.0},
    Ability.SPEED: {"scrap": 5, "energy": 2.0},
    Ability.SHIELD: {"scrap": 10, "energy": 1.0},
    Ability.LOCKPICK:  {"scrap": 10, "energy": 1.5},
}
