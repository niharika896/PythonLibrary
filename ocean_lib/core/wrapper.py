from typing import List, Optional
from ..models.game_state import GameState
from ..models.entities import Bot, Algae, Bank, EnergyPad, VisibleScrap
from ..models.point import Point
from ..common.constants import Direction, Ability
from ..common.utils import manhattan_distance
from .action import Action, MoveAction, HarvestAction, AttackAction, SpawnAction, SelfDestructAction

class BotWrapper:
    """
    Wraps a Bot and the GameState to provide a convenient API for strategy implementation.
    """
    def __init__(self, bot: Bot, game_state: GameState):
        self.bot = bot
        self.game_state = game_state
        self.game = None # Injected by Game loop

    @property
    def id(self) -> int:
        return self.bot.id

    @property
    def location(self) -> Point:
        return self.bot.location
    
    @property
    def energy(self) -> int:
        return self.bot.energy

    @property
    def scraps(self) -> int:
        return self.bot.scraps

    # ---- Sensing with Radius ----

    def get_my_bots(self) -> List[Bot]:
        return self.game_state.my_bots

    def get_visible_enemies(self) -> List[Bot]:
        return self.game_state.visible_entities.enemies
    
    def get_enemies_in_radius(self, radius: int) -> List[Bot]:
        return [
            b for b in self.get_visible_enemies() 
            if manhattan_distance(self.location, b.location) <= radius
        ]

    def get_visible_algae(self) -> List[Algae]:
        return self.game_state.visible_entities.algae + self.game_state.permanent_entities.algae

    def get_algae_in_radius(self, radius: int) -> List[Algae]:
        return [
            a for a in self.get_visible_algae()
            if manhattan_distance(self.location, a.location) <= radius
        ]

    def get_visible_scraps(self) -> List[VisibleScrap]:
        return self.game_state.visible_entities.scraps

    def get_banks(self) -> List[Bank]:
        return self.game_state.permanent_entities.banks

    def get_nearest_bank(self) -> Optional[Bank]:
        banks = self.get_banks()
        if not banks:
            return None
        return min(banks, key=lambda b: manhattan_distance(self.location, b.location))
    
    def get_nearest_algae(self) -> Optional[Algae]:
        algae = self.get_visible_algae()
        if not algae:
            return None
        return min(algae, key=lambda a: manhattan_distance(self.location, a.location))

    def get_nearest_enemy(self) -> Optional[Bot]:
        enemies = self.get_visible_enemies()
        if not enemies:
            return None
        return min(enemies, key=lambda e: manhattan_distance(self.location, e.location))

    # ---- Actions ----

    def move(self, direction: Direction, step: int = 1) -> MoveAction:
        """
        Moves the bot. 
        Set step=2 if you have speed ability and want to move 2 blocks.
        """
        return MoveAction(direction=direction, step=step)

    def harvest(self, direction: Direction) -> HarvestAction:
        return HarvestAction(direction=direction)

    def attack(self, target: Point) -> AttackAction:
        """Attacks a specific coordinate."""
        return AttackAction(target=target)

    def self_destruct(self) -> SelfDestructAction:
        return SelfDestructAction()
    
    def direction_to(self, target: Point) -> Direction:
        """
        Returns the primary cardinal direction.
        (Previously moveTarget from BotContext roughly matches this logic)
        """
        dx = target.x - self.location.x
        dy = target.y - self.location.y
        if abs(dx) >= abs(dy):
            return Direction.EAST if dx > 0 else Direction.WEST
        else:
            return Direction.NORTH if dy > 0 else Direction.SOUTH

    def spawn(self, abilities: List[Ability], strategy: 'BotStrategy', location: Optional[Point] = None) -> SpawnAction:
        if self.game:
            return self.game.spawn(abilities, strategy, location)
        return SpawnAction(abilities=abilities, spawn_location=location, new_bot_id=-1) # Should fail/warn
