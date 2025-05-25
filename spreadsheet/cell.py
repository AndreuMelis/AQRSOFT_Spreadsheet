from content.cell_content import CellContent
from typing import Union, List, Any

class Cell:
    def __init__(self, coordinate: tuple, content: CellContent = None):
        self._coordinate = coordinate
        self._content = content

    @property
    def coordinate(self) -> tuple:
        return self._coordinate
    
    @coordinate.setter
    def coordinate(self, value: tuple) -> None:
        self._coordinate = value

    @property
    def content(self) -> CellContent:
        return self._content
    
    @content.setter
    def content(self, content: CellContent) -> None:
        self._content = content

    # Thanks to abstract class CellContent
    def get_value(self):
        return self.content.get_value()
    
    # def store_content_in_cell(self):

class Number:
    def __init__(self, value: Union[int, float]):
        self._value = value
    
    @property
    def value(self) -> Union[int, float]:
        return self._value

    @value.setter
    def value(self, value: Union[int, float]):
        self._value = value
    
    def get_value(self):
        return self._value

class Coordinate:
    def __init__(self, column: str, row: int):
        self._row = row
        self._column = column

    @property
    def column(self) -> str:
        return self._column

    @column.setter
    def column(self, value: str) -> None:
        self._column = value

    @property
    def row(self) -> int:
        return self._row

    @row.setter
    def row(self, value: int) -> None:
        self._row = value

class Number:
    def __init__(self, value: Union[int, float]):
        self._value = value
    
    @property
    def value(self) -> Union[int, float]:
        return self._value

    @value.setter
    def value(self, value: Union[int, float]):
        self._value = value
    
    def get_value(self):
        return self._value


