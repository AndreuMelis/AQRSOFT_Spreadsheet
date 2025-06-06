# spreadsheet/dependency_manager.py

from typing import Set, Dict
from exceptions import CircularDependencyException

class DependencyManager:
    def __init__(self):
        # Maps "A1" -> {"B2", "C3", ...}
        self.dependency_graph: Dict[str, Set[str]] = {}

    def check_circular_dependencies(self, current_cell: str, referenced_cells: Set[str]):
        """
        Raise CircularDependencyException if any referenced_cells introduce a cycle
        back to current_cell.
        """
        visited = set()

        def visit(cell: str):
            if cell == current_cell:
                raise CircularDependencyException(f"Circular dependency detected at {cell}")
            if cell in visited:
                return
            visited.add(cell)
            for neighbor in self.dependency_graph.get(cell, []):
                visit(neighbor)

        for ref in referenced_cells:
            visit(ref)

    def update_dependencies(self, current_cell: str, referenced_cells: Set[str]):
        """
        After ensuring no cycle, record the new edges into the dependency_graph.
        """
        self.dependency_graph[current_cell] = referenced_cells
