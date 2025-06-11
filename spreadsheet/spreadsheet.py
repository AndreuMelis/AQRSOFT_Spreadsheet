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
            
            # Find the actual cell using LIST iteration
            for cell in self.cells:
                current_cell_name = f"{cell.coordinate.column}{cell.coordinate.row}"
                if current_cell_name == cell_name:
                    # SAFER: Only set _computed_value to None instead of calling invalidate_value()
                    if hasattr(cell.content, '_computed_value'):
                        cell.content._computed_value = None
                        
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
        """Print the spreadsheet in a formatted table view."""
        if not self.cells:
            print("(empty spreadsheet)")
            return

        # Get coordinates from the cell list instead of dictionary keys
        sorted_coords = sorted([cell.coordinate for cell in self.cells], 
                            key=lambda c: (c.row, c.column))
        
        if not sorted_coords:
            print("(empty spreadsheet)")
            return

        # Find bounds
        min_row = min(coord.row for coord in sorted_coords)
        max_row = max(coord.row for coord in sorted_coords)
        min_col = min(coord.column for coord in sorted_coords)
        max_col = max(coord.column for coord in sorted_coords)
        
        # Generate column range
        def next_column(col):
            if col == 'Z':
                return 'AA'
            elif col.endswith('Z'):
                prefix = col[:-1]
                return next_column(prefix) + 'A'
            else:
                return col[:-1] + chr(ord(col[-1]) + 1)
        
        columns = []
        current_col = min_col
        while True:
            columns.append(current_col)
            if current_col == max_col:
                break
            current_col = next_column(current_col)
        
        # Calculate column widths
        col_widths = {}
        for col in columns:
            max_width = len(col)  # Header width
            for row in range(min_row, max_row + 1):
                coord = Coordinate(col, row)
                cell = self.get_cell(coord)
                if cell:
                    # Get calculated value for display
                    try:
                        if hasattr(cell.content, 'formula'):  # It's a formula
                            if hasattr(cell.content, 'get_value'):
                                content_str = str(cell.content.get_value(self))
                            else:
                                content_str = str(cell.get_textual_representation())
                        else:
                            # For other content, try without spreadsheet parameter
                            if hasattr(cell.content, 'get_value'):
                                content_str = str(cell.content.get_value())
                            else:
                                content_str = str(cell.get_textual_representation())
                    except Exception:
                        content_str = str(cell.get_textual_representation())
                    
                    max_width = max(max_width, len(content_str))
            col_widths[col] = max_width
        
        # Print header
        print("   ", end="")
        for col in columns:
            print(f" {col:^{col_widths[col]}} ", end="")
        print()
        
        # Print top border
        print("  ┌", end="")
        for i, col in enumerate(columns):
            print("─" * (col_widths[col] + 2), end="")
            if i < len(columns) - 1:
                print("┬", end="")
        print("┐")
        
        # Print rows
        for row in range(min_row, max_row + 1):
            print(f"{row:2}│", end="")
            for col in columns:
                coord = Coordinate(col, row)
                cell = self.get_cell(coord)
                if cell:
                    # Same logic as above for displaying values
                    try:
                        if hasattr(cell.content, 'formula'):  # It's a formula
                            if hasattr(cell.content, 'get_value'):
                                content = str(cell.content.get_value(self))
                            else:
                                content = str(cell.get_textual_representation())
                        else:
                            if hasattr(cell.content, 'get_value'):
                                content = str(cell.content.get_value())
                            else:
                                content = str(cell.get_textual_representation())
                    except Exception:
                        content = str(cell.get_textual_representation())
                else:
                    content = ""
                print(f" {content:^{col_widths[col]}} │", end="")
            print()
            
            # Print row separator (except for last row)
            if row < max_row:
                print("  ├", end="")
                for i, col in enumerate(columns):
                    print("─" * (col_widths[col] + 2), end="")
                    if i < len(columns) - 1:
                        print("┼", end="")
                print("┤")
        
        # Print bottom border
        print("  └", end="")
        for i, col in enumerate(columns):
            print("─" * (col_widths[col] + 2), end="")
            if i < len(columns) - 1:
                print("┴", end="")
        print("┘")