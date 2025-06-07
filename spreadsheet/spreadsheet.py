# spreadsheet/spreadsheet.py

import re
from typing import Dict, Set
from spreadsheet.cell import Cell
from spreadsheet.coordinate import Coordinate
from spreadsheet.dependency_manager import DependencyManager

class Spreadsheet:
    def __init__(self):
        # Diccionario: clave = Coordinate, valor = Cell
        self.cells: Dict[Coordinate, Cell] = {}

    def get_cell(self, coords: Coordinate) -> Cell | None:
        return self.cells.get(coords)
    
    def get_cell_name(self, content) -> str:
        """
        Given a CellContent instance, find the Coordinate key whose cell has that content,
        and return its string name (e.g. "C2"). Raises ValueError if not found.
        """
        for coord, cell in self.cells.items():
            if cell.content is content:
                return f"{coord.column}{coord.row}"
        raise ValueError("Cell containing this content was not found.")
    
    def is_valid_cell_reference(self, token: str) -> bool:
        """
        Returns True if token matches e.g. 'A1', 'B2', etc.
        """
        return bool(re.fullmatch(r"[A-Z]+\d+", token))

    def get_dependency_manager(self) -> DependencyManager:
        """
        Return (or create) the DependencyManager instance for this spreadsheet.
        """
        if not hasattr(self, "_dep_manager"):
            self._dep_manager = DependencyManager()
        return self._dep_manager

    def add_cell(self, coords: Coordinate, cell: Cell) -> None:
        self.cells[coords] = cell

    def print_spreadsheet(self) -> None:
        # Convert column letters to numeric index for proper ordering
        def col_to_num(col: str) -> int:
            num = 0
            for c in col:
                num = num * 26 + (ord(c) - ord('A') + 1)
            return num

        # Sort coordinates by row then column
        sorted_coords = sorted(self.cells.keys(), key=lambda c: (c.row, col_to_num(c.column)))
        rows = sorted({coord.row for coord in sorted_coords})
        columns = sorted({coord.column for coord in sorted_coords}, key=lambda c: col_to_num(c))

        # Header
        print("\t" + "\t".join(columns))
        # Rows
        for row in rows:
            row_values = []
            for column in columns:
                coord = Coordinate(column, row)
                if coord in self.cells:
                    cell = self.get_cell(coord)
                    try:
                        value = cell.content.get_value(self)
                    except Exception as e:
                        value = f"Error: {e}"
                    row_values.append(value)
                else:
                    row_values.append('')
            print(f"{row}\t" + "\t".join(str(v) for v in row_values))
