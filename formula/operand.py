from postfix_evaluator import FormulaElementVisitor, FormulaElement
from abc import ABC, abstractmethod
from typing import Union, Any, List, Dict, Type
from spreadsheet.cell import Number, Cell
from spreadsheet.coordinate import Coordinate
from spreadsheet.spreadsheet import Spreadsheet
from formula.function import Function, FunctionArgument, SUMA, PROMEDIO, MAX, MIN # Import specific function classes

class Operand(FormulaElement):
    @abstractmethod
    def get_value(self):
        """Each operand type implements its own value resolution logic"""
        pass

    def accept(self, visitor: FormulaElementVisitor) -> Any:
        return visitor.visit_operand(self)
    
    @classmethod
    @abstractmethod
    def create_from_token(cls, token_value, spreadsheet=None) -> 'Operand':
        """Factory method to create operand from token"""
        pass

class NumericOperand(Operand):
    """Represents numeric literal values"""
    
    def __init__(self, value: Union[int, float]) -> None:
        self.value: Number = Number(value)

    def get_value(self) -> Number:
        return self.value.get_value()
    
    @classmethod
    def create_from_token(cls, token_value, spreadsheet=None) -> 'NumericOperand':
        """Create NumericOperand from token value"""
        if '.' in str(token_value):
            return cls(float(token_value))
        else:
            return cls(int(token_value))

class CellOperand(Operand):
    """Represent a cell from the spreadsheet"""
    
    def __init__(self, cell: Cell) -> None:
        self.cell = cell

    def get_value(self):
        return self.cell.get_value()
    
    @classmethod
    def create_from_token(cls, token_value, spreadsheet: Spreadsheet = None) -> 'CellOperand':
        """Create CellOperand from cell reference token"""
        cell = Cell.from_token(token_value, spreadsheet)
        return cls(cell)
    
# TODO -> Done: RangeCell should not be an operand, its a function argument
# class RangeOperand(Operand):
#     """Represents a range of cells (e.g., A1:B3)"""
    
#     def __init__(self, start_cell: Cell, end_cell: Cell) -> None:
#         self.start_cell = start_cell
#         self.end_cell = end_cell
    
#     def get_value(self):
#         """Returns a list of values from the range"""
#         # This would need to be implemented based on your Cell/Spreadsheet structure
#         # For now, returning a placeholder
#         return [self.start_cell.get_value(), self.end_cell.get_value()]
    
#     @classmethod
#     def create_from_token(cls, token_value, spreadsheet=None) -> 'RangeOperand':
#         """Create RangeOperand from range reference token"""
#         if spreadsheet is None:
#             raise ValueError("Spreadsheet is required to create RangeOperand")
        
#         # Parse range reference (e.g., "A1:B3")
#         start_ref, end_ref = str(token_value).split(':')
        
#         # Create start and end cells using CellOperand logic
#         start_cell_operand = CellOperand.create_from_token(start_ref, spreadsheet)
#         end_cell_operand = CellOperand.create_from_token(end_ref, spreadsheet)
        
#         return cls(start_cell_operand.cell, end_cell_operand.cell)

# TODO
class FunctionOperand(Operand):
    """Represents spreadsheet functions like SUM, MIN, MAX"""
    
    def __init__(self, func: Function, arguments: List[FunctionArgument] = None) -> None:
        self.function: Function = func
        self.arguments: List[FunctionArgument] = arguments or []

    def get_value(self, spreadsheet=None):
        values = []
        for arg in self.arguments:
            v = arg.get_value(spreadsheet)
            if isinstance(v, list):
                values.extend(v)
            else:
                values.append(v)
        return self.function.evaluate(values)
    
    @classmethod
    def create_from_token(cls, token_value, spreadsheet=None) -> 'FunctionOperand':
        """Create FunctionOperand from function name token"""
        
        function_name = str(token_value).upper()
        
        # Map function names to their respective classes
        function_map: Dict[str, Type[Function]] = {
            "SUMA": SUMA,
            "SUM": SUMA, # Assuming SUM also maps to SUMA
            "PROMEDIO": PROMEDIO,
            "AVERAGE": PROMEDIO, # Assuming AVERAGE also maps to PROMEDIO
            "MAX": MAX,
            "MIN": MIN,
        }

        if function_name in function_map:
            func = function_map[function_name]() # Instantiate the specific function class
            return cls(func)
        else:
            raise ValueError(f"Unknown function: {function_name}")