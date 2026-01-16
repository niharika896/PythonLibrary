from abc import ABC, abstractmethod

class BotController(ABC):
    """
    Base class for all bot strategies.
    """

    TEMPLATE: str | None = None

    def __init__(self, ctx):
        self.ctx = ctx

    @abstractmethod
    def act(self):
        pass

    @classmethod
    def spawn(cls, abilities: list[str], location: int):
        """
        User-friendly spawn helper.

        Returns:
            dict: Spawn specification for wrapper.
        """
        if cls.TEMPLATE is None:
            raise ValueError(f"{cls.__name__} has no TEMPLATE defined")

        return {
            "strategy": cls,
            "abilities": abilities,
            "location": location,
        }
