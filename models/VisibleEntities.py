from .Bot import Bot
from .Point import Point
from .VisibleScrap import VisibleScrap
from typing import List

class VisibleEntities:
    enemies: List[Bot]
    scraps: List[VisibleScrap]
