from typing import List, Optional, TYPE_CHECKING, Any

from ocean_lib.core.strategy import BotStrategy
from ..models.game_state import GameState
from ..models.entities import Bot, Algae, Bank, EnergyPad, VisibleScrap
from ..models.point import Point
from ..common.constants import Direction, Ability
from ..common.utils import manhattan_distance
from .action import Action, MoveAction, HarvestAction, AttackAction, SpawnAction, SelfDestructAction

class BotContext:
    """
    Wraps a Bot and the GameState to provide a convenient API for strategy implementation.
    Actions are automatically appended to the runner's action list.
    """
    def __init__(self, bot: Bot, game_state: GameState):
        self.bot = bot
        self.game_state = game_state
        self._pending_actions: List[Action] = []

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
        Action is automatically added to the current tick's action list.
        """
        action = MoveAction(direction=direction, step=step)
        self._pending_actions.append(action)
        return action

    def harvest(self, direction: Direction) -> HarvestAction:
        """
        Harvests a resource in the given direction.
        Action is automatically added to the current tick's action list.
        """
        action = HarvestAction(direction=direction)
        self._pending_actions.append(action)
        return action

    def attack(self, target: Point) -> AttackAction:
        """
        Attacks a specific coordinate.
        Action is automatically added to the current tick's action list.
        """
        action = AttackAction(target=target)
        self._pending_actions.append(action)
        return action

    def self_destruct(self) -> SelfDestructAction:
        """
        Self-destructs the bot.
        Action is automatically added to the current tick's action list.
        """
        action = SelfDestructAction()
        self._pending_actions.append(action)
        return action

    def direction_to(self, target: Point) -> Direction:
        """
        Returns the primary cardinal direction.
        """
        dx = target.x - self.location.x
        dy = target.y - self.location.y
        if abs(dx) >= abs(dy):
            return Direction.EAST if dx > 0 else Direction.WEST
        else:
            return Direction.NORTH if dy > 0 else Direction.SOUTH

    def spawn(self, capabilities: List[Ability], strategy: BotStrategy, location: Point) -> SpawnAction:
        """
        Spawns a new bot with the given capabilities and strategy.
        Action is automatically added to the current tick's action list.
        """
        # new_bot_id is temporary here, will be overwritten by Game
        action = SpawnAction(abilities=capabilities, strategy=strategy, spawn_location=location, new_bot_id=-1)
        self._pending_actions.append(action)
        return action
