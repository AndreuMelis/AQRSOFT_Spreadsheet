# --------------------------------------------------------------------------------------------------
# Archivo: spreadsheet/spreadsheet.py
# --------------------------------------------------------------------------------------------------
from .cell import Cell
from .coordinate import Coordinate
import re
from typing import List

class Spreadsheet:
    def __init__(self):
        # Diccionario: clave = Coordinate, valor = Cell
        self.cells: dict[Coordinate, Cell] = {}

    def get_cell(self, coords: Coordinate) -> Cell | None:
        return self.cells.get(coords)
    
    def add_cell(self, coords: Coordinate, cell: Cell) -> None:
        self.cells[coords] = cell

    # Parse a fórmula para extraer referencias de celdas (p. ej. “A1”, “B2”)
    def parse_formula(self, formula_str: str) -> list[str]:
        return re.findall(r'[A-Z]+\d+', formula_str)
    
    def print_spreadsheet(self) -> None:
        # Ordena las coordenadas por (fila, columna)
        sorted_coords = sorted(self.cells.keys(), key=lambda c: (c.row, c.column))
        # Extrae todos los números de fila y letras de columna únicos
        rows = sorted({coord.row for coord in sorted_coords})
        columns = sorted({coord.column for coord in sorted_coords})

        # Primera línea: encabezados de columna
        print("\t" + "\t".join(columns))
        for row in rows:
            row_values = []
            for column in columns:
                coord = Coordinate(column, row)
                if coord in self.cells:
                    cell = self.get_cell(coord)
                    # Al pedir el valor, le pasamos la propia hoja (self)
                    value = cell.content.get_value(self)
                    row_values.append(value)
                else:
                    row_values.append('')
            print(f"{row}\t" + "\t".join(str(v) for v in row_values))
