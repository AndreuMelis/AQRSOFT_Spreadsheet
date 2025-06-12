from spreadsheet.cell import Cell
from spreadsheet.coordinate import Coordinate
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spreadsheet.spreadsheet import Spreadsheet
import re
from typing import Union, List, Any, Tuple

class CellRange:
    def __init__(self, origin: str, destination: str) -> None:
        self.origin_cell = origin.upper()
        self.dest_cell   = destination.upper()
        
    def get_values(self, spreadsheet: 'Spreadsheet') -> List[Cell]:
        """
        Returns a list of cells in the range from origin_cell to dest_cell (inclusive).
        """

        def parse_ref(ref):
            match = re.match(r'^([A-Z]+)(\d+)$', ref)
            if not match:
                raise ValueError(f"Invalid cell reference: {ref}")
            col_str, row_str = match.groups()
            return col_str, int(row_str)

        origin_col, origin_row = parse_ref(self.origin_cell)
        dest_col, dest_row = parse_ref(self.dest_cell)

        if origin_col > dest_col or origin_row > dest_row:
            raise ValueError("Start cell must be before or the same as end cell")

        def col_to_num(col):
            num = 0
            for c in col:
                num = num * 26 + (ord(c) - ord('A') + 1)
            return num

        def num_to_col(num):
            col = ''
            while num > 0:
                num, rem = divmod(num - 1, 26)
                col = chr(rem + ord('A')) + col
            return col

        start_col_num = col_to_num(origin_col)
        end_col_num = col_to_num(dest_col)
        start_row = min(origin_row, dest_row)
        end_row = max(origin_row, dest_row)
        start_col_num, end_col_num = min(start_col_num, end_col_num), max(start_col_num, end_col_num)

        values = []
        for col_num in range(start_col_num, end_col_num + 1):
            col_str = num_to_col(col_num)
            for row in range(start_row, end_row + 1):
                coord = Coordinate(col_str, row)
                cell = spreadsheet.get_cell(coord)
                if cell:
                    values.append(cell)
        return values