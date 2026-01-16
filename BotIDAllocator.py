class BotIDAllocator:
    """
    bot ID generator.
    """
    def __init__(self, start: int = 1):
        self._next_id = start

    def allocate(self) -> int:
        bot_id = self._next_id
        self._next_id += 1
        return bot_id
