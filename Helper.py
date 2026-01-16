from .models.Point import Point
from  .Constants import Direction

def manhattan_distance(p1:Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def next_point(p: Point, d: Direction):
    if d == Direction.NORTH:
        return Point(p.x, p.y + 1)
    if d == Direction.SOUTH:
        return Point(p.x, p.y - 1)
    if d == Direction.EAST:
        return Point(p.x + 1, p.y)
    if d == Direction.WEST:
        return Point(p.x - 1, p.y)
    
def direction_from_point(p1: Point, p2: Point) -> Direction:
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    if abs(dx) >= abs(dy):
        return Direction.EAST if dx > 0 else Direction.WEST
    else:
        return Direction.NORTH if dy > 0 else Direction.SOUTH