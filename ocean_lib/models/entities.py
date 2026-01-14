from dataclasses import dataclass
from typing import List, Optional
from ..common.constants import Ability
from .point import Point

@dataclass
class Entity:
    """Base class for all entities on the map."""
    location: Point

@dataclass
class Algae(Entity):
    """Resource entity that can be harvested."""
    is_poison: Optional[bool] = None
    pass

@dataclass
class Bank(Entity):
    """Structure where resources can be deposited."""
    id: int
    deposit_occuring: int
    deposit_amount: int
    deposit_owner: int
    depositticksleft: int

@dataclass
class EnergyPad(Entity):
    """Structure that recharges bot energy."""
    id: int
    available: int
    ticksleft: int

@dataclass
class VisibleScrap(Entity):
    """Scrap dropped on the ground."""
    amount: int = 1

@dataclass
class Bot(Entity):
    """Represents a bot in the game."""
    id: int
    owner_id: int
    energy: int
    scraps: int
    abilities: List[Ability]
    algae_held: int