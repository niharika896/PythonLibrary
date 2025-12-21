from .BotBase import BotController
from ..Constants import Direction
from ..models import Point

class HeatSeeker(BotController):

    def __init__(self, ctx, target: Point):
        super().__init__(ctx)
        self.target = target

    #Position helpers
    def at_target(self) -> bool:
        loc = self.ctx.getLocation()
        return loc.x == self.target.x and loc.y == self.target.y

    def delta_to_target(self):
        loc = self.ctx.getLocation()
        return self.target.x - loc.x, self.target.y - loc.y

    #Movement helpers
    def move_towards_x(self):
        dx, _ = self.delta_to_target()
        if dx > 0:
            return self.ctx.move(Direction.EAST)
        if dx < 0:
            return self.ctx.move(Direction.WEST)

    def move_towards_y(self):
        _, dy = self.delta_to_target()
        if dy > 0:
            return self.ctx.move(Direction.NORTH)
        if dy < 0:
            return self.ctx.move(Direction.SOUTH)

    # attack
    def self_destruct(self):
        return self.ctx.selfDestruct()
