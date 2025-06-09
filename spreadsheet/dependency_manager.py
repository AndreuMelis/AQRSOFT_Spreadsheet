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
        # First check direct circular dependency
        if current_cell in referenced_cells:
            raise CircularDependencyException(f"Circular dependency detected: {current_cell} references itself")
        
        # Then check indirect circular dependencies
        visited = set()
        path = set()

        def has_cycle_to_current(cell: str) -> bool:
            if cell == current_cell:
                return True
            if cell in path:  # Found a cycle, but not to current_cell
                return False
            if cell in visited:
                return False
                
            visited.add(cell)
            path.add(cell)
            
            # Check all dependencies of this cell
            for neighbor in self.dependency_graph.get(cell, set()):
                if has_cycle_to_current(neighbor):
                    return True
                    
            path.remove(cell)
            return False

        # Check if any of the referenced cells can reach back to current_cell
        for ref_cell in referenced_cells:
            if has_cycle_to_current(ref_cell):
                raise CircularDependencyException(f"Circular dependency detected: {current_cell} -> {ref_cell} -> ... -> {current_cell}")

    def update_dependencies(self, current_cell: str, referenced_cells: Set[str]):
        """
        After ensuring no cycle, record the new edges into the dependency_graph.
        """
        self.dependency_graph[current_cell] = referenced_cells.copy()