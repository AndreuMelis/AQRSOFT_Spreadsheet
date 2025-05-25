from postfix_evaluator import FormulaElementVisitor, FormulaElement
from formula.function import Function, FunctionArgument
from abc import ABC, abstractmethod
from typing import Union, Any, List
from spreadsheet.cell import Number, Cell

class Operand(FormulaElement):
    @abstractmethod
    def get_value(self, spreadsheet = None):
        """Each operand type implements its own value resolution logic"""
        pass

    def accept(self, visitor: FormulaElementVisitor) -> Any:
        return visitor.visit_operand(self)

class NumericOperand(Operand):
    """Represents numeric literal values"""
    
    def __init__(self, value: Union[int, float]) -> None:
        self.value: Number = Number(value)

    def get_value(self, spreadsheet = None) -> Number:
        return self.value.get_value()

class CellOperand(Operand):
    """Represent a cell from the spreadsheet"""
    
    def __init__(self, cell: Cell) -> None:
        self.cell = cell

    def get_value(self, spreadsheet = None):
        return self.cell.get_value()
    
class FunctionOperand(Operand):
    """Represents spreadsheet functions like SUM, MIN, MAX"""
    
    def __init__(self, func: Function, arguments: List[FunctionArgument]) -> None:
        self.function: Function = func
        self.arguments: List[FunctionArgument] = arguments

    def get_value(self, spreadsheet = None):
        values = []
        for arg in self.arguments:
            v = arg.get_value(spreadsheet)
            if isinstance(v, list):
                values.extend(v)
            else:
                values.append(v)
        return self.function.evaluate(values)