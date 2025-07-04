from abc import ABC, abstractmethod
from typing import Any, List, Union, Optional
from spreadsheet.cell import Cell
from content.number import Number
from spreadsheet.cell_range import CellRange
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spreadsheet.spreadsheet import Spreadsheet
    import re
from formula.operand import FunctionOperand


class Function(ABC):
    @abstractmethod
    def evaluate(self, arguments: List[Any]) -> Any:
        pass

class SUMA(Function):
    """
    Computes the sum of all arguments.
    """
    def evaluate(self, arguments: List[Any]) -> Any:
        total = 0
        for value in arguments:
            total += value
        return total

class MAX(Function):
    """
    Returns the maximum value among arguments, or 0 if no arguments.
    """
    def evaluate(self, arguments: List[Any]) -> Any:
        if not arguments:
            return 0
        max_val = arguments[0]
        for value in arguments[1:]:
            if value > max_val:
                max_val = value
        return max_val

class MIN(Function):
    """
    Returns the minimum value among arguments, or 0 if no arguments.
    """
    def evaluate(self, arguments: List[Any]) -> Any:
        if not arguments:
            return 0
        min_val = arguments[0]
        for value in arguments[1:]:
            if value < min_val:
                min_val = value
        return min_val

class PROMEDIO(Function):
    """
    Returns the arithmetic mean of arguments, or 0 if no arguments.
    """
    def evaluate(self, arguments: List[Any]) -> Any:
        count = 0
        total = 0
        for value in arguments:
            total += value
            count += 1
        return total / count if count > 0 else 0



# Function argument types
class FunctionArgument(ABC):
    """Base class for function arguments"""
    @abstractmethod
    def get_value():
        pass
    
class CellArgument(FunctionArgument):
    def __init__(self, cell: Cell) -> None:
        self.cell = cell

    def get_value(self): 
        return self.cell.get_value()
    
    @classmethod
    def create_from_token(cls, token_value, spreadsheet: 'Spreadsheet' = None) -> 'CellArgument':
        """Create CellOperand from cell reference token"""
        cell = Cell.from_token(token_value, spreadsheet)
        return cls(cell)

class CellRangeArgument(FunctionArgument):
    """
    Returns the values of all the cells inside the range
    """
    def __init__(self, origin: str, destination: str, spreadsheet: 'Spreadsheet') -> None:
        self.cell_range: CellRange = CellRange(origin, destination)
        self.cells: List[Cell] = self.cell_range.get_values(spreadsheet)
    
    def get_value(self) -> List:
        """
        Returns a list of values for all cells in the range."""
        return [cell.get_value() for cell in self.cells]

class NumericArgument(FunctionArgument):
    def __init__(self, value: Union[int, float]) -> None:
        super().__init__()
        self.value: Number = Number(value)
    
    def get_value(self) -> Number:
        return self.value.get_value()
    
class FunctionArgumentWrapper(FunctionArgument):
    """Wrapper to treat a FunctionOperand as a FunctionArgument for nested functions"""
    
    def __init__(self, function_operand: FunctionOperand):
        self.function_operand = function_operand
    
    def get_value(self):
        return self.function_operand.get_value()

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