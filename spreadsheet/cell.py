from content.cell_content import CellContent
from spreadsheet.spreadsheet import Spreadsheet
from typing import Union, List, Any
class Cell:
    def __init__(self, coordinate: tuple, content: CellContent = None):
        self._coordinate = Coordinate(coordinate[0], coordinate[1])
        self._content = content

    # TODO -> check how return of coordinates is needed
    @property
    def coordinate(self) -> tuple:
        return self._coordinate
    
    @coordinate.setter
    def coordinate(self, coordinate: tuple) -> None:
        self._coordinate = Coordinate(coordinate[0], coordinate[1])

    @property
    def content(self) -> CellContent:
        return self._content
    
    @content.setter
    def content(self, content: CellContent) -> None:
        self._content = content

    # Thanks to abstract class CellContent
    def get_value(self):
        return self.content.get_value()
    
    @staticmethod
    def from_token(token_value, spreadsheet: Spreadsheet = None) -> 'Cell':
        """Create Cell from cell reference token"""
        if spreadsheet is None:
            raise ValueError("Spreadsheet is required to create CellOperand")

        # Parse cell reference (e.g., "A1" -> column=0, row=0)
        import re
        match = re.match(r'^([A-Z]+)(\d+)$', str(token_value))
        if not match:
            raise ValueError(f"Invalid cell reference: {token_value}")
        
        col_str, row_str = match.groups()
        coords = Coordinate(col_str, int(row_str))
        
        cell = spreadsheet.get_cell(coords)
        return cell
    
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
    def __init__(self, column: str, row: str):
        self._row = row
        self._column = column

    @property
    def column(self) -> str:
        return self._column

    @column.setter
    def column(self, value: str) -> None:
        self._column = value

    @property
    def row(self) -> str:
        return self._row

    @row.setter
    def row(self, value: str) -> None:
        self._row = value