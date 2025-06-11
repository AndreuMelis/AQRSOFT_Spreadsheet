# spreadsheet/spreadsheet.py

import re
from typing import Dict, Set, List, Optional
from spreadsheet.cell import Cell
from spreadsheet.coordinate import Coordinate
from spreadsheet.dependency_manager import DependencyManager

class Spreadsheet:
    def __init__(self):
        self.cells: List[Cell] = []
        self.dep_manager = DependencyManager()

    def get_cell(self, coords: Coordinate) -> Optional[Cell]:
        for cell in self.cells:
            if cell.coordinate == coords:
                return cell
        return None
    
    def get_cell_name(self, content) -> str:
        """Find the cell name that contains the given content."""
        for cell in self.cells:
            if cell.content is content:
                return f"{cell.coordinate.column}{cell.coordinate.row}"
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
        """Add a cell to the spreadsheet at the given coordinates."""
        # FIXED: Set coordinate properly
        if cell.coordinate != coords:
            cell.coordinate = coords  # This will use the fixed setter
        
        # Remove existing cell at these coordinates
        self._remove_cell_at_coords(coords)
        
        # Add the new cell to the list
        self.cells.append(cell)
        
        # Invalidate dependent formulas
        cell_name = f"{coords.column}{coords.row}"
        self._invalidate_dependent_formulas(cell_name)

    def _remove_cell_at_coords(self, coords: Coordinate):
        """Remove existing cell at coordinates."""
        for i, cell in enumerate(self.cells):
            if cell.coordinate == coords:
                self.cells.pop(i)
                return

    def _invalidate_dependent_formulas(self, changed_cell_name: str):
        """Invalidate formulas that depend on the changed cell."""
        # Check each formula cell to see if it depends on the changed cell
        for cell in self.cells:  # CHANGED: iterate through list instead of dict
            if hasattr(cell.content, '_get_referenced_cells_from_tokens'):
                # If it's a formula, check if it references the changed cell
                try:
                    referenced_cells = cell.content._get_referenced_cells_from_tokens()
                    if changed_cell_name in referenced_cells:
                        cell.content.invalidate_value()
                except:
                    # If there's any error, just invalidate to be safe
                    cell.content.invalidate_value()
            elif hasattr(cell.content, 'invalidate_value'):
                # For older formula style, invalidate all formulas (safe approach)
                if hasattr(cell.content, 'formula'):  # Check if it's a formula
                    cell.content.invalidate_value()

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