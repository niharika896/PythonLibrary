from .EnemyBot import EnemyBot
from .VisibleAlgae import VisibleAlgae
from .VisibleScrap import VisibleScrap
from typing import List

class VisibleEntities:
    enemies: List[EnemyBot]
    algae: List[VisibleAlgae]
    scraps: List[VisibleScrap]
