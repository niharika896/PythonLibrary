import json
from typing import Dict, Any
from .Constants import ActionType

class Action:
    def __init__(self, action_type: ActionType, payload: Dict[str, Any]):
        self.action_type = action_type
        self.payload = payload

    def emit(self):
        out = {"action": self.action_type.value}
        out.update(self.payload)
        print(json.dumps(out)) ##read by go using stdout

