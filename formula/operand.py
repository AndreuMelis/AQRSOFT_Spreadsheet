from abc import ABC, abstractmethod
from cell import Cell
from exceptions import EvaluationErrorException
from formula.functions import Function, FunctionArgument

class Operand(ABC):
    @abstractmethod
    def get_value(self, spreadsheet=None):
        pass

class NumericOperand(Operand):
    def __init__(self, value):
        # TODO: Store numeric value
        pass

    def get_value(self, spreadsheet=None):
        # TODO: Return numeric literal
        pass

class CellOperand(Operand):
    def __init__(self, cell: Cell):
        # TODO: Store cell reference
        pass

    def get_value(self, spreadsheet=None):
        # TODO: Retrieve value from spreadsheet cell
        pass

class FunctionOperand(Operand):
    def __init__(self, func: Function, arguments: list):
        # TODO: Store function and its arguments
        pass

    def get_value(self, spreadsheet=None):
        # TODO: Evaluate function over argument values
        pass
