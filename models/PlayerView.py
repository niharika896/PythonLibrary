from .Bot import Bot
from .VisibleEntities import VisibleEntities
from .PermanentEntities import PermanentEntities
from typing import List
    
class PlayerView:
    tick: int
    scraps: int
    algae: int
    bot_count: int
    max_bots: int
    width: int
    height: int
    bots: List[Bot]
    visible_entities: VisibleEntities
    permanent_entities: PermanentEntities
