from abc import ABC, abstractmethod
from typing import Any, List, Union, Optional
from spreadsheet.cell import Cell
from content.number import Number
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
    def __init__(self, start_ref: str, end_ref: str):
        self.start_ref = start_ref.upper()
        self.end_ref   = end_ref.upper()

    def get_value(self, spreadsheet):
        """
        Return a list of numbers corresponding to the cells in the range.
        E.g. 'A1:A3' → [ value(A1), value(A2), value(A3) ].
        """
        # Use your CellRange class to get the Cell objects in that rectangle
        cell_objs = CellRange(self.start_ref, self.end_ref).get_values(spreadsheet)
        # Extract each cell’s computed value
        return [
            cell.content.get_value(spreadsheet)
            for cell in cell_objs
            if cell and cell.content is not None
        ]

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