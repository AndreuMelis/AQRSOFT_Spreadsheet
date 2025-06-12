from abc import ABC, abstractmethod
from typing import Union

class CellContent(ABC):
    @abstractmethod
    def get_value(self):
        pass
    @abstractmethod
    def get_text(self) -> str:
        pass
        