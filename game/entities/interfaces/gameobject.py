from abc import ABC, abstractmethod


class GameObject(ABC):
    """Interface of objects that could kill."""

    # @abstractmethod
    # def __init__(self, x, y):
    #     self.x = x
    #     self.y = y

    @abstractmethod
    def draw(self, surface):
        """Draw cuurrent object on passed surface."""
        pass
        