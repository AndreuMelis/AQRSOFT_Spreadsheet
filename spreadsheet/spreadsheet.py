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
        self.dep_manager = DependencyManager()

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

    # def get_dependency_manager(self) -> DependencyManager:
    #     """
    #     Return (or create) the DependencyManager instance for this spreadsheet.
    #     """
    #     if not hasattr(self, "_dep_manager"):
    #         self._dep_manager = DependencyManager()
    #     return self._dep_manager

    def add_cell(self, coords: Coordinate, cell: Cell) -> None:
        """Add a cell and invalidate dependent formulas"""
        cell_name = f"{coords.column}{coords.row}"
        
        # Add the new cell
        self.cells[coords] = cell
        
        # Invalidate any formulas that reference this cell
        self._invalidate_dependent_formulas(cell_name)

    def _invalidate_dependent_formulas(self, changed_cell_name: str):
        """
        Find all formulas that reference the changed cell and invalidate their computed values.
        This forces them to recalculate when next accessed.
        """        
        # Get all cells that depend on the changed cell
        dependent_cells = []
        for cell_name, dependencies in self.dep_manager.dependency_graph.items():
            if changed_cell_name in dependencies:
                dependent_cells.append(cell_name)
        
        # Invalidate all dependent formulas (transitively)
        visited = set()
        to_invalidate = dependent_cells[:]
        
        while to_invalidate:
            cell_name = to_invalidate.pop(0)
            if cell_name in visited:
                continue
                
            visited.add(cell_name)
            
            # Find the actual cell and invalidate it if it's a formula
            for coord, cell in self.cells.items():
                if f"{coord.column}{coord.row}" == cell_name:
                    if hasattr(cell.content, 'invalidate_value'):
                        cell.content.invalidate_value()
                        
                        # Add cells that depend on this cell to the invalidation queue
                        for other_cell, other_deps in self.dep_manager.dependency_graph.items():
                            if cell_name in other_deps and other_cell not in visited:
                                to_invalidate.append(other_cell)
                    break

    def set_cell_content(self, coords: Coordinate, content):
        """Convenience method to set cell content"""
        from spreadsheet.cell import Cell
        
        cell = Cell(coords, content)
        self.add_cell(coords, cell)

    def print_spreadsheet(self) -> None:
        """
        Render the current spreadsheet to the terminal, catching any evaluation
        errors per-cell and displaying them inline without mutating state.
        """
        if not self.cells:
            print("(empty spreadsheet)")
            return

        # Determine all rows and columns present
        sorted_coords = sorted(self.cells.keys(), key=lambda c: (c.row, c.column))
        rows = sorted({coord.row for coord in sorted_coords})
        columns = sorted({coord.column for coord in sorted_coords}, key=lambda col: [ord(c) for c in col])

        # Header
        print("\t" + "\t".join(columns))

        # Body
        for row in rows:
            display_vals = []
            for col in columns:
                coord = Coordinate(col, row)
                cell = self.cells.get(coord)
                if cell:
                    try:
                        val = cell.get_value(self)
                    except Exception as e:
                        val = f"Error: {e}"
                else:
                    val = ''
                display_vals.append(str(val))

            print(f"{row}\t" + "\t".join(display_vals))