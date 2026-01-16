from .Constants import Direction, Ability, ABILITY_COSTS
from .Translate import *
from .models import Point
from .Helper import *

class BotContext:
    """
    BotContext provides a safe, read-only interface between a bot strategy
    and the game engine state.

    It exposes:
    - bot status
    - sensing utilities
    - movement/pathfinding helpers
    - combat and resource actions

    A BotContext instance is created once per bot per tick.
    """

    def __init__(self, api, bot):
        """
        Initialize the context for a single bot.

        Args:
            api (GameAPI): Read-only game API wrapper.
            bot (Bot): Bot model instance representing the current bot.
        """
        self.api = api
        self.bot = bot

    # ==================== ROBOT STATUS ====================

    def getID(self) -> int:
        """
        Get the unique identifier of this bot.

        Returns:
            int: Unique bot ID assigned by the engine.
        """
        return self.bot.id
    
    def getEnergy(self) -> int:
        """
        Get the current energy level of the bot.

        Returns:
            int: Current energy units.
        """
        return self.bot.energy

    def getLocation(self) -> Point:
        """
        Get the current grid position of the bot.

        Returns:
            Point: Bot's current location.
        """
        return self.bot.location

    def getAlgaeHeld(self) -> int:
        """
        Get the amount of algae currently carried by the bot.

        Returns:
            int: Algae units held.
        """
        return self.bot.algae_held

    def getType(self) -> list[str]:
        """
        Get the list of abilities currently equipped by the bot.

        Returns:
            list[str]: Ability identifiers.
        """
        return self.bot.abilities

    def cost(self, abilities: list[str]) -> dict:
        """
        Calculate the resource cost of spawning or upgrading abilities.

        Applies ability synergies where applicable.

        Args:
            abilities (list[str]): List of ability identifiers.

        Returns:
            dict: Dictionary with keys:
                - 'scrap' (int)
                - 'energy' (float)
        """
        total_scrap = 0
        total_energy = 0.0

        for ability in abilities:
            if ability not in ABILITY_COSTS:
                continue
            total_scrap += ABILITY_COSTS[ability]["scrap"]
            total_energy += ABILITY_COSTS[ability]["energy"]

        # HeatSeeker synergy discount
        if "SPEED" in abilities and "SELF_DESTRUCT" in abilities:
            total_scrap -= 5

        return {"scrap": total_scrap, "energy": total_energy}

    # ==================== SENSING ====================

    def senseEnemyNearby(self):
        """
        Get all visible enemy bots.

        Returns:
            list[Bot]: Visible enemy bots.
        """
        return self.api.visible_enemies()

    def senseEnemyinRadius(self, bot: Point, radius: int = 1):
        """
        Detect enemies within a Manhattan radius of a given point.

        Args:
            bot (Point): Center position.
            radius (int): Manhattan distance radius.

        Returns:
            list[Bot]: Enemies within radius.
        """
        return [
            b for b in self.api.visible_enemies()
            if manhattan_distance(b.location, bot) <= radius
        ]

    def senseBotNearby(self):
        """
        Get friendly bots excluding this bot.

        Returns:
            list[Bot]: Nearby friendly bots.
        """
        return [b for b in self.api.get_my_bots() if b.id != self.bot.id]

    def senseBotinRadius(self, bot: Point, radius: int = 1):
        """
        Detect friendly bots within a radius of a point.

        Args:
            bot (Point): Center position.
            radius (int): Manhattan distance radius.

        Returns:
            list[Bot]: Friendly bots within radius.
        """
        return [
            b for b in self.api.get_my_bots()
            if b.id != self.bot.id and manhattan_distance(b.location, bot) <= radius
        ]

    def senseAlgae(self, radius: int = 1):
        """
        Detect visible algae within a radius of the bot.

        Args:
            radius (int): Manhattan distance radius.

        Returns:
            list[Algae]: Algae entities within radius.
        """
        pos = self.bot.location
        return [
            a for a in self.api.visible_algae()
            if manhattan_distance(a.location, pos) <= radius
        ]

    def senseSacraps(self, radius: int = 1):
        """
        Detect visible scrap resources within a radius of the bot.

        Args:
            radius (int): Manhattan distance radius.

        Returns:
            list[Scrap]: Scrap entities within radius.
        """
        pos = self.bot.location
        return [
            a for a in self.api.visible_scraps()
            if manhattan_distance(a.location, pos) <= radius
        ]

    def senseObjects(self):
        """
        Retrieve all static and resource objects visible to the player.

        Returns:
            dict: Mapping of object categories to entity lists.
        """
        return {
            "scraps": self.api.sense_bot_scraps(),
            "banks": self.api.banks(),
            "energypads": self.api.energypads(),
        }

    def senseWalls(self):
        """
        Get all visible walls.

        Returns:
            list[Wall]: Visible wall entities.
        """
        return self.api.visible_walls()

    def senseWallsinRadius(self, bot: Point, radius: int = 1):
        """
        Detect walls within a Manhattan radius of a point.

        Args:
            bot (Point): Center position.
            radius (int): Manhattan distance radius.

        Returns:
            list[Wall]: Walls within radius.
        """
        return [
            w for w in self.api.visible_walls()
            if manhattan_distance(w, bot) <= radius
        ]

    # ==================== PATHING ====================

    def canMove(self, direction: Direction) -> bool:
        """
        Check whether movement in a given direction stays within map bounds.

        Args:
            direction (Direction): Intended movement direction.

        Returns:
            bool: True if move is inside map bounds.
        """
        x, y = self.bot.location.x, self.bot.location.y

        if direction == Direction.NORTH:
            y += 1
        elif direction == Direction.SOUTH:
            y -= 1
        elif direction == Direction.EAST:
            x += 1
        elif direction == Direction.WEST:
            x -= 1

        return 0 <= x < self.api.view.width and 0 <= y < self.api.view.height

    def move(self, direction: Direction):
        """
        Create a move action in the given direction.

        Args:
            direction (Direction): Direction to move.

        Returns:
            Action: MOVE action.
        """
        return move(direction)

    def shortestPath(self, target: Point) -> int:
        """
        Compute Manhattan distance to a target point.

        Args:
            target (Point): Target location.

        Returns:
            int: Manhattan distance.
        """
        bx, by = self.bot.location.x, self.bot.location.y
        return abs(bx - target.x) + abs(by - target.y)

    # ==================== COLLISION AVOIDANCE ====================

    def checkBlocked(self, pos: Point) -> bool:
        """
        Determine if a position is blocked by any obstacle.

        Args:
            pos (Point): Position to check.

        Returns:
            bool: True if blocked.
        """
        return (
            self.senseWallsinRadius(pos) or
            self.senseEnemyinRadius(pos) or
            self.senseBotinRadius(pos)
        )

    def moveTarget(self, bot: Point, target: Point):
        """
        Determine the safest direction to move toward a target.

        Args:
            bot (Point): Current position.
            target (Point): Target position.

        Returns:
            Direction | None: Chosen direction or None if blocked.
        """
        dx = target.x - bot.x
        dy = target.y - bot.y

        primary = (
            Direction.EAST if dx > 0 else Direction.WEST
            if abs(dx) >= abs(dy)
            else Direction.NORTH if dy > 0 else Direction.SOUTH
        )

        next_pos = next_point(bot, primary)
        if not self.checkBlocked(next_pos):
            return primary

        for d in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            if not self.checkBlocked(next_point(bot, d)):
                return d

        return None

    def moveTargetSpeed(self, bot: Point, target: Point):
        """
        Determine a safe speed move toward a target.

        Args:
            bot (Point): Current position.
            target (Point): Target position.

        Returns:
            tuple[Direction | None, int]: Direction and step count.
        """
        dx = target.x - bot.x
        dy = target.y - bot.y

        primary = (
            Direction.EAST if dx > 0 else Direction.WEST
            if abs(dx) >= abs(dy)
            else Direction.NORTH if dy > 0 else Direction.SOUTH
        )

        p1 = next_point(bot, primary)
        if not self.checkBlocked(p1):
            p2 = next_point(p1, primary)
            return (primary, 2) if not self.checkBlocked(p2) else (primary, 1)

        for d in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            p1 = next_point(bot, d)
            if not self.checkBlocked(p1):
                return (d, 2) if not self.checkBlocked(next_point(p1, d)) else (d, 1)

        return None, 0

    # ==================== COMBAT ====================

    def canDefend(self) -> bool:
        """
        Check if the bot has defensive capability.

        Returns:
            bool: True if SHIELD ability exists.
        """
        return Ability.SHIELD.value in self.bot.abilities

    def defendSelf(self):
        """
        Create a defend action.

        Returns:
            Action: DEFEND action.
        """
        return defend()

    def selfDestruct(self):
        """
        Create a self-destruct action.

        Returns:
            Action: SELF_DESTRUCT action.
        """
        return self_destruct()

    # ==================== SPAWNING ====================

    def canSpawn(self, abilities: list[str]) -> bool:
        """
        Check whether spawning a bot with given abilities is possible.

        Args:
            abilities (list[str]): Ability list.

        Returns:
            bool: True if spawn is allowed.
        """
        if self.api.view.bot_count >= self.api.view.max_bots:
            return False
        return self.api.get_scraps() >= self.cost(abilities)["scrap"]

    # ==================== RESOURCE HELPERS ====================

    def harvestAlgae(self, direction: Direction):
        """
        Create a harvest action in a direction.

        Args:
            direction (Direction): Harvest direction.

        Returns:
            Action: HARVEST action.
        """
        return harvest(direction)

    # ==================== NEAREST OBJECT HELPERS ====================

    def getNearestBank(self) -> Point:
        """Return nearest bank location."""
        pos = self.bot.location
        return min(self.api.banks(), key=lambda b: manhattan_distance(b.location, pos)).location

    def getNearestEnergyPad(self) -> Point:
        """Return nearest energy pad location."""
        pos = self.bot.location
        return min(self.api.energypads(), key=lambda p: manhattan_distance(p.location, pos)).location

    def getNearestScrap(self) -> Point:
        """Return nearest scrap location."""
        pos = self.bot.location
        return min(self.api.sense_bot_scraps(), key=lambda s: manhattan_distance(s.location, pos)).location

    def getNearestAlgae(self) -> Point:
        """Return nearest algae location."""
        pos = self.bot.location
        return min(self.api.visible_algae(), key=lambda a: manhattan_distance(a.location, pos)).location

    def getNearestEnemy(self) -> Point:
        """Return nearest enemy location."""
        pos = self.bot.location
        return min(self.api.visible_enemies(), key=lambda e: manhattan_distance(e.location, pos)).location
