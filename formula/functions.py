from abc import ABC, abstractmethod
from typing import Any, List, Union, Optional
from cell import Cell, Number, CellRange

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

class PROMEDIO(Function):
    def evaluate(self, arguments: List[Any]) -> Any:
        return sum(arguments) / len(arguments) if arguments else 0


# Function argument types
class FunctionArgument(ABC):
    """Base class for function arguments"""
    pass

class CellArgument(FunctionArgument):
    def __init__(self, cell: Cell) -> None:
        self.cell = cell

    def get_value(self, spreadsheet = None): 
        """ 
        Spreadsheet needed to match with CellRangeArgument get_values()
        """
        return self.cell.get_value()

class CellRangeArgument(FunctionArgument):
    """
    Returns teh values of all the cells inside the range
    """
    def __init__(self, origin: str, destination: str) -> None:
        self.cell_range: CellRange = CellRange(origin, destination)
    
    def get_value(self, spreadsheet_context):
        return self.cell_range.get_values(spreadsheet_context)

class NumericArgument(FunctionArgument):
    def __init__(self, value: Union[int, float]) -> None:
        super().__init__()
        self.value: Number = Number(value)
    
    def get_value(self, spreadsheet = None) -> Number:
        return self.value.get_value()
# TODO 
class FunctionEvaluator:
    def __init__(self):
        pass