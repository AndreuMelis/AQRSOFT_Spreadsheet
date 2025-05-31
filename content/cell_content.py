from abc import ABC, abstractmethod
from typing import Union
from spreadsheet.cell import Number

class CellContent(ABC):
    @abstractmethod
    def get_value(self):
        pass
        