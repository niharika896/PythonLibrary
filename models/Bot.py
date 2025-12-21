from typing import List
from .Point import Point
from ..Constants import Ability, BotType



class Bot:
    id: int
    owner_id: int
    location: Point
    template : BotType
    energy: int
    scraps: int
    abilities: List[Ability]
    vision_radius: int
