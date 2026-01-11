from .Action import Action
from .Constants import ActionType, Direction, Ability
from .models.Algae import VisibleAlgae

def move(bot_id: int, direction: Direction):
    return Action(ActionType.MOVE, {
        "bot_id": bot_id,
        "direction": direction.value
    })


def harvest(bot_id: int, visibleAlgae: VisibleAlgae):
    return Action(ActionType.HARVEST, {
        "bot_id": bot_id,
        "visibleAlgae": visibleAlgae
    })


def poison(bot_id: int, x: int, y: int):
    return Action(ActionType.POISON, {
        "bot_id": bot_id,
        "x": x,
        "y": y
    })


def self_destruct(bot_id: int):
    return Action(ActionType.SELF_DESTRUCT, {
        "bot_id": bot_id
    })


def attack(bot_id: int, x: int, y: int):
    return Action(ActionType.ATTACK, {
        "bot_id": bot_id,
        "x": x,
        "y": y
    })


def defend(bot_id: int):
    return Action(ActionType.DEFEND, {
        "bot_id": bot_id
    })


def lockpick(bot_id: int, bank_id: int):
    return Action(ActionType.LOCKPICK, {
        "bot_id": bot_id,
        "bank_id": bank_id
    })


def scavenge(bot_id: int, direction: Direction):
    return Action(ActionType.SCAVENGE, {
        "bot_id": bot_id,
        "direction": direction.value
    })


def transfer_energy(bot_id: int, target_bot_id: int):
    return Action(ActionType.TRANSFER_ENERGY, {
        "bot_id": bot_id,
        "target_bot_id": target_bot_id
    })


def spawn(template_name: str, abilities: list[str]):
    return Action(ActionType.SPAWN, {
        "template": template_name,
        "abilities": abilities
    })

def moveSpeed(bot_id: int, direction: Direction, step:int):
    return Action(ActionType.MOVE, {
        "bot_id": bot_id,
        "direction": direction.value,
        "step": step
    })
    

# def upgrade(bot_id: int, ability: Ability):
#     return Action(ActionType.UPGRADE, {
#         "bot_id": bot_id,
#         "ability": ability.value
#     })

#Example Usage:
#move(1, Direction.NORTH)
#upgrade(2, Ability.SHIELD)
