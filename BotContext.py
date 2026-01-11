from .Constants import Direction, Ability, ABILITY_COSTS
from .Translate import *
from .models import Point
from .Helper import *


class BotContext:
    def __init__(self, api, bot):
        self.api = api
        self.bot = bot

    # ---------------- Robot Status ----------------
    def getID(self): #OK
        return self.bot.id

    def getHealth(self):
        return self.bot.energy

    def getLocation(self) -> Point:
        return self.bot.location

    def getType(self):
        return self.bot.abilities

    def cost(self, abilities: list[str]) -> dict:
        total_scrap = 0
        total_energy = 0.0

        for ability in abilities:
            if ability not in ABILITY_COSTS:
                continue

            total_scrap += ABILITY_COSTS[ability]["scrap"]
            total_energy += ABILITY_COSTS[ability]["energy"]

        # ---- Synergy: Heatseeker (SPEED + SELF_DESTRUCT) ----
        if "SPEED" in abilities and "SELF_DESTRUCT" in abilities:
            total_scrap -= 5

        return {
            "scrap": total_scrap,
            "energy": total_energy,
        }

    # ---------------- Sensing ----------------
    def senseEnemyNearby(self):
        return self.api.visible_enemies()
    
    def senseEnemyinRadius(self, bot:Point, radius: int = 1):
        return [b for b in self.api.visible_enemies() if manhattan_distance(b.location,bot)<=radius]

    def senseBotNearby(self):
        return [b for b in self.api.get_my_bots() if b.id != self.bot.id]
    
    def senseBotinRadius(self, bot:Point, radius: int = 1):
        return [b for b in self.api.get_my_bots() if b.id != self.bot.id and manhattan_distance(b.location,bot)<=radius]
    
    def senseAlgae(self, radius: int = 1):
        pos=self.bot.location
        return [a for a in self.api.visible_algae() if manhattan_distance(a.location,pos)<=radius]

    def senseObjects(self):
        return {
            "scraps": self.api.sense_bot_scraps(),
            "banks": self.api.banks(),
            "energypads": self.api.energypads(),
        }

    def senseWalls(self):
        return self.api.visible_walls()
    
    def senseWallsinRadius(self, bot:Point, radius: int = 1):
        return [w for w in self.api.visible_walls() if manhattan_distance(w,bot)<=radius]

    # ---------------- Pathing ----------------
    def canMove(self, direction: Direction):
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
        return move(self.bot.id, direction)
    

    def shortestPath(self, target: Point) -> int:
        bx, by = self.bot.location.x, self.bot.location.y
        tx, ty = target.x, target.y
        return abs(bx - tx) + abs(by - ty)
    
    # ---------------Collision Avoidance----------------
    
    def checkBlocked(self,pos: Point):
        return (
            self.senseWallsinRadius(pos) or
            self.senseEnemyinRadius(pos) or
            self.senseBotinRadius(pos)
        )
        
    def moveTarget(self, bot: Point, target: Point):
        dx = target.x - bot.x
        dy = target.y - bot.y

        if abs(dx) >= abs(dy):
            primary = Direction.EAST if dx > 0 else Direction.WEST
        else:
            primary = Direction.NORTH if dy > 0 else Direction.SOUTH
        
        # ---------- try intended direction ----------
        next_pos = next_point(bot, primary)
        if not self.checkBlocked(next_pos):
            return primary

        # ---------- fallback: any safe direction ----------
        for d in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            np = next_point(bot, d)
            if not self.checkBlocked(np):
                return d

        # ---------- no safe move ----------
        return None
    
    # SPPEEEDDD
    
    def moveTargetSpeed(self, bot: Point, target: Point):
        dx = target.x - bot.x
        dy = target.y - bot.y

        # ---------- determine primary direction ----------
        if abs(dx) >= abs(dy):
            primary = Direction.EAST if dx > 0 else Direction.WEST
        else:
            primary = Direction.NORTH if dy > 0 else Direction.SOUTH

        # ---------- try primary direction ----------
        p1 = next_point(bot, primary)
        if not self.checkBlocked(p1):
            p2 = next_point(p1, primary)
            if not self.checkBlocked(p2):
                return primary, 2   # fast move
            return primary, 1       # single step

        # ---------- fallback directions ----------
        for d in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            p1 = next_point(bot, d)
            if not self.checkBlocked(p1):
                p2 = next_point(p1, d)
                if not self.checkBlocked(p2):
                    return d, 2
                return d, 1

        # ---------- no safe movement ----------
        return None, 0

    
    
    # ---------------- Combat ----------------
    def canDefend(self):
        return Ability.SHIELD.value in self.bot.abilities 

    def defend(self):
        return defend(self.bot.id)

    def selfDestruct(self):
        return self_destruct(self.bot.id)

    # ---------------- Spawning & Upgrading ----------------
    def canSpawn(self, abilities: list[str]) -> bool:
        if self.api.view.bot_count >= self.api.view.max_bots:
            return False
        cost = self.cost(abilities)
        return self.api.get_scraps() >= cost["scrap"]


    def spawn(self, template: str, abilities: list[str]):
        return spawn(template, abilities)

    # ---------------- Resource Gathering ----------------
    def isAlgae(self, location: Point):
        return any(a.location == location for a in self.api.visible_algae())

    def harvestAlgae(self, direction: Direction):
        return harvest(self.bot.id, direction)

    def checkPoisonous(self, direction: Direction):
        bx, by = self.bot.location.x, self.bot.location.y

        if direction == Direction.NORTH:
            target = Point(bx, by + 1)
        elif direction == Direction.SOUTH:
            target = Point(bx, by - 1)
        elif direction == Direction.EAST:
            target = Point(bx + 1, by)
        else:
            target = Point(bx - 1, by)

        for algae in self.api.visible_algae():
            if algae.location == target:
                return algae.is_poison

        return False
    
    # -----------------Extra Utilities -----------------
    
        
