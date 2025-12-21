# oceanmaster/bots/custom.py

from .BotBase import BotController

class CustomBot(BotController):

    def act(self):
        pass

#sample usage:
# from ..Helper import spawn
# from ..Constants import Ability

# actions.append(
#     spawn(
#         "CustomBot",
#         [
#             Ability.HARVEST.value,
#             Ability.SCOUT.value,
#             Ability.SPEED.value,
#         ]
#     )
# )
