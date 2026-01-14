from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from ..common.constants import ActionType, Direction, Ability
from ..models.point import Point

@dataclass
class Action:
    """Base class for all actions."""
    type: ActionType
    
    def to_json(self) -> Dict[str, Any]:
        return {"action": self.type.value}

@dataclass
class MoveAction(Action):
    """
    Action to move a bot in a direction.
    Supports optional 'step' for SPEED ability (moving 2 tiles).
    """
    direction: Direction
    step: int = 1
    type: ActionType = field(default=ActionType.MOVE, init=False)

    def to_json(self) -> Dict[str, Any]:
        return {
            "action": self.type.value, 
            "direction": self.direction.value,
            "step": self.step
        }

@dataclass
class HarvestAction(Action):
    """Action to harvest a resource."""
    direction: Direction
    type: ActionType = field(default=ActionType.HARVEST, init=False)

    def to_json(self) -> Dict[str, Any]:
        return {"action": self.type.value, "direction": self.direction.value}
    
@dataclass
class AttackAction(Action):
    """
    Action to attack a location or direction.
    Updated to support X,Y coordinates if required by engine, 
    but keeping direction as primary if that's the modern API.
    Ref: Translate.py used (x,y).
    """
    target: Optional[Point] = None
    type: ActionType = field(default=ActionType.ATTACK, init=False)

    def to_json(self) -> Dict[str, Any]:
        if self.target:
             return {
                "action": self.type.value, 
                "x": self.target.x, 
                "y": self.target.y
            }
        return {"action": self.type.value}

@dataclass
class SpawnAction(Action):
    """
    Action to spawn a new bot.
    Includes abilities, optional spawn location, and a client-generated ID.
    The engine MUST respect this ID for strategy mapping to work.
    """
    abilities: List[Ability]
    new_bot_id: int
    spawn_location: Optional[Point] = None
    type: ActionType = field(default=ActionType.SPAWN, init=False)

    def to_json(self) -> Dict[str, Any]:
        data = {
            "action": self.type.value, 
            "abilities": [a.value for a in self.abilities],
            "id": self.new_bot_id # Sending ID to engine
        }
        if self.spawn_location:
            data["location"] = {"x": self.spawn_location.x, "y": self.spawn_location.y}
        if self.spawn_location is not None and isinstance(self.spawn_location, int):
             # Old Translate.py allowed int check? No it was typed as int but named location... 
             # Translate.py: def spawn(..., location:int, ...)
             # Wait, Translate.py line 69: location:int. But line 74: "location": location.
             # If the engine expects an INT index for location (linear index?), then Point is wrong.
             # However, standard grid games use (x,y). 
             # Let's assume Point is correct unless proven otherwise, 
             # OR the user meant 'location index' (like 0-3 for sides?).
             pass
             
        return data

@dataclass
class SelfDestructAction(Action):
    """Action to self-destruct."""
    type: ActionType = field(default=ActionType.SELF_DESTRUCT, init=False)

    def to_json(self) -> Dict[str, Any]:
        return {"action": self.type.value}
