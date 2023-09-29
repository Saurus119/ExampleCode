from abc import ABC, abstractmethod
from typing import Union

class IRedis(ABC):

    @abstractmethod
    def get(self, key: str) -> str:
        """Return cached value."""
        pass

    @abstractmethod
    def update_or_create(self, key: str, value: Union[str, dict, list, int]) -> str:
        """if not exists, create it."""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> str:
        """Remove cached value"""
        pass