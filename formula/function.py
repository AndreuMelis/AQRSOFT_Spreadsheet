from abc import ABC, abstractmethod
from typing import Any, List, Union, Optional
from spreadsheet.cell import Cell, Number
from spreadsheet.cell_range import CellRange
from spreadsheet.spreadsheet import Spreadsheet
import re

# Abstract base for all spreadsheet functions
# TODO -> implement the function methods
class Function(ABC):
    @abstractmethod
    def evaluate(self, arguments: List[Any]) -> Any:
        pass

class SUMA(Function):
    def evaluate(self, arguments: List[Any]) -> Any:
        return sum(arguments)

class MAX(Function):
    def evaluate(self, arguments: List[Any]) -> Any:
        return max(arguments)

class MIN(Function):
    def evaluate(self, arguments: List[Any]) -> Any:
        return min(arguments)

class PROMEDIO(Function):
    def evaluate(self, arguments: List[Any]) -> Any:
        return sum(arguments) / len(arguments) if arguments else 0


# Function argument types
class FunctionArgument(ABC):
    """Base class for function arguments"""
    @abstractmethod
    def get_value(self, spreadsheet = None):
        pass
class CellArgument(FunctionArgument):
    def __init__(self, cell: Cell) -> None:
        self.cell = cell

    def get_value(self, spreadsheet = None): 
        """ 
        Spreadsheet needed to match with CellRangeArgument get_values()
        """
        return self.cell.get_value()
    
    @classmethod
    def create_from_token(cls, token_value, spreadsheet: Spreadsheet = None) -> 'CellArgument':
        """Create CellOperand from cell reference token"""
        cell = Cell.from_token(token_value, spreadsheet)
        return cls(cell)

class CellRangeArgument(FunctionArgument):
    """
    Returns teh values of all the cells inside the range
    """
    def __init__(self, origin: str, destination: str, spreadsheet: Spreadsheet) -> None:
        self.cell_range: CellRange = CellRange(origin, destination)
        self.cells: List[Cell] = self.cell_range.get_values(spreadsheet)
    
    def get_values(self):
        """
        TODO-> ceck if to return list of cell values or list of cells
        """
        return self.cells # [cell.get_value() for cell in self.cells]

class NumericArgument(FunctionArgument):
    def __init__(self, value: Union[int, float]) -> None:
        super().__init__()
        self.value: Number = Number(value)
    
    def get_value(self, spreadsheet = None) -> Number:
        return self.value.get_value()

class FunctionEvaluator:
    """
    Utility for quick evaluation of simple formulas by regex.
    """
    @staticmethod
    def evaluate_max_operand(formula: str) -> float:
        operands = [float(o) for o in re.findall(r'\b\d+(\.\d+)?\b', formula)]
        return max(operands) if operands else 0.0

    @staticmethod
    def evaluate_min_operand(formula: str) -> float:
        operands = [float(o) for o in re.findall(r'\b\d+(\.\d+)?\b', formula)]
        return min(operands) if operands else 0.0