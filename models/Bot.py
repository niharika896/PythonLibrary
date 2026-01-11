from typing import List
from .Point import Point
from ..Constants import Ability, BotType



class Bot:
    id: int
    owner_id: int
    location: Point
    energy: int
    scraps: int
    abilities: List[Ability]