from cell_content import CellContent
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


class CellRange:
    def __init__(self, origin: str, destination: str) -> None:
        self.origin_cell = origin.upper()
        self.dest_cell   = destination.upper()

    def _col_to_index(self, col: str) -> int:
        """
        Convert column letters (e.g. 'A', 'Z', 'AA') to 1-based index.
        """
        idx = 0
        for c in col:
            idx = idx * 26 + (ord(c) - ord('A') + 1)
        return idx

    def _index_to_col(self, idx: int) -> str:
        """
        Convert 1-based column index back to letters.
        """
        letters = []
        while idx:
            idx, rem = divmod(idx - 1, 26)
            letters.append(chr(rem + ord('A')))
        return ''.join(reversed(letters))

    def _split_coord(self, coord: str) -> (str, int):
        """
        Split 'BC23' → ('BC', 23)
        """
        col = ''.join(ch for ch in coord if ch.isalpha())
        row = ''.join(ch for ch in coord if ch.isdigit())
        return col, int(row)

    def get_cells(self, spreadsheet) -> List[Cell]:
        """
        Return all Cell objects in the rectangular range from origin to destination.
        """
        col1, row1 = self._split_coord(self.origin_cell)
        col2, row2 = self._split_coord(self.dest_cell)

        c1 = self._col_to_index(col1)
        c2 = self._col_to_index(col2)
        r1, r2 = min(row1, row2), max(row1, row2)
        c1, c2 = min(c1, c2), max(c1, c2)

        cells: List[Cell] = []
        for ci in range(c1, c2 + 1):
            col_letter = self._index_to_col(ci)
            for r in range(r1, r2 + 1):
                cells.append(spreadsheet.get_cell((col_letter, r)))
        return cells

    def get_values(self, spreadsheet) -> List[Any]:
        """
        Return the evaluated values of each cell in the range.
        """
        return [cell.get_value(spreadsheet) for cell in self.get_cells(spreadsheet)]