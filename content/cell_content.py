from abc import ABC, abstractmethod
from typing import Union
from cell import Number

class CellContent(ABC):
    @abstractmethod
    def get_value(self):
        pass

class TextContent(CellContent):
    def __init__(self, text: str):
        super().__init__()
        self.text: str = text

    def get_value(self):
        return self.text

class NumericContent(CellContent):
    def __init__(self, value: Union[int, float]):
        super().__init__()
        self.number: Number = Number(value)

    def get_value(self):
        return self.number.get_value()
        
        