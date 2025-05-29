from spreadsheet.cell import Cell
from spreadsheet.coordinate import Coordinate
import re
# TODO -> check what is needed in compute formula when passing a spreadsheet
class Spreadsheet():
    def __init__(self):
        self.cells = {}

    def get_cell(self, coords: Coordinate) -> Cell:
        return self.cells.get(coords)
    
    def add_cell(self, coords: Coordinate, cell: Cell) -> None:
        self.cells[coords] = cell

    # Parse a formula string and extract all cell references
    def parse_formula(self, formula_str):
        return re.findall(r'[A-Z]+\d+', formula_str)
    
    def print_spreadsheet(self):
        sorted_coords = sorted(self.cells.keys(), key=lambda c: (c.row, c.column))
        rows = sorted({coord.row for coord in sorted_coords})
        columns = sorted({coord.column for coord in sorted_coords})

        print("\t" + "\t".join(columns))
        for row in rows:
            row_values = []
            for column in columns:
                coord = Coordinate(column, row)
                if coord in self.cells:
                    cell = self.get_cell(coord)
                    # the spreadsheet is passed to the get_value of each content type
                    value = cell.content.get_value(self)
                    row_values.append(value)
                else:
                    row_values.append('')
            print(f"{row}\t" + "\t".join(str(value) for value in row_values))
