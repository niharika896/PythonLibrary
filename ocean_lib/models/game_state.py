from dataclasses import dataclass
from typing import List, Dict
from .entities import Bot, Algae, VisibleScrap, Bank, EnergyPad
from .point import Point

@dataclass
class VisibleEntities:
    """Entities currently visible to the player's bots."""
    enemies: List[Bot]
    algae: List[Algae]
    scraps: List[VisibleScrap]
    walls: List[Point]

@dataclass
class PermanentEntities:
    """Static entities that do not move."""
    banks: List[Bank]
    energypads: List[EnergyPad]
    algae: List[Algae]

@dataclass
class GameState:
    """
    Represents the full view of the game state visible to the player.
    """
    tick: int
    scraps: int
    algae: int
    bot_count: int
    max_bots: int
    width: int
    height: int
    my_bots: List[Bot]
    visible_entities: VisibleEntities
    permanent_entities: PermanentEntities
