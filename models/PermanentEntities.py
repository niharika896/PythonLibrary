from .Bank import Bank
from .EnergyPad import EnergyPad
from typing import List
from .Point import Point
from .Algae import Algae

class PermanentEntities:
    banks: List[Bank]
    energypads: List[EnergyPad]
    walls: List[Point]
    algae: List[Algae]
