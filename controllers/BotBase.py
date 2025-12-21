from abc import ABC, abstractmethod

class BotController(ABC):
    def __init__(self, ctx):
        self.ctx = ctx

    @abstractmethod
    def act(self):
        pass
