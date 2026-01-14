from ..models.point import Point

def manhattan_distance(p1: Point, p2: Point) -> int:
    """Calculates the Manhattan distance between two points."""
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)
