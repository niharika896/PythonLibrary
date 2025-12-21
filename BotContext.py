from .Constants import Direction, Ability, ABILITY_COSTS
from .Helper import *
from .models import Point


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

    def senseBotNearby(self):
        return [b for b in self.api.get_my_bots() if b.id != self.bot.id]

    def senseAlgae(self):
        return self.api.visible_algae()

    def senseObjects(self):
        return {
            "scraps": self.api.sense_bot_scraps(),
            "banks": self.api.banks(),
            "energypads": self.api.energypads(),
        }

    def senseWalls(self):
        pass

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

    # ---------------- Combat ----------------
    def canAttack(self, location: Point): #How to Define this? #does it have energy?
        pass

    def attack(self, location: Point):
        return attack(self.bot.id, location.x, location.y)

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
    # def canAffordUpgrade(self, ability: str) -> bool:
    #     if ability in self.bot.abilities:
    #         return False

    #     cost = self.cost([ability])

    #     return (
    #         self.api.get_scraps() >= cost["scrap"]
    #         and self.bot.energy >= cost["energy"]
    #     )



    # def upgrade(self, ability: Ability):
    #     return upgrade(self.bot.id, ability)

    # def giveNew(self, ability: Ability):
    #     return upgrade(self.bot.id, ability)

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
