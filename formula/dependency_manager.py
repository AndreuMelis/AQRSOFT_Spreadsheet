from spreadsheet.cell import Cell
from spreadsheet.spreadsheet import Spreadsheet
from exceptions import CircularDependencyException

class DependencyManager:
    def __init__(self):
        self.dependency_graph = {}  # Maps 'A1' -> set('B2', 'C3', ...)

    def check_circular_dependencies(self, current_cell: str, referenced_cells: set[str]):
        visited = set()

        def visit(cell):
            if cell == current_cell:
                raise CircularDependencyException(f"Circular dependency detected at {cell}")
            if cell in visited:
                return
            visited.add(cell)
            for neighbor in self.dependency_graph.get(cell, []):
                visit(neighbor)

        for ref in referenced_cells:
            visit(ref)

    def update_dependencies(self, current_cell: str, referenced_cells: set[str]):
        """ Updates the dependency graph after formula evaluation. """
        self.dependency_graph[current_cell] = referenced_cells