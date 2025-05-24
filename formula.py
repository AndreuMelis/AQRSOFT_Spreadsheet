from cell_content import CellContent
from cell import Number, Cell
from function import Function
from abc import ABC, abstractmethod
from typing import Any, List, Union, Optional
from function import FunctionArgument

# TODO -> define FormulaContent completely, tokenizer, parser, evaluate function, perform operation...
"""
Main idea: el Evaluate postfix expression visitor diferencia entre operand i operator,
per tant, utilitzant inheritance d'operand, puc obtenir el valor de cada subclasse d'operand
amb el corresponent get_value concret
"""
# Incomplete, just for clarity
# May substitute FormulaController defined in the documents
class FormulaContent(CellContent):
    def __init__(self, formula: str) -> None:
        super().__init__()
        self.formula: str = formula
        self.operands: List['Operand'] = []
        self.operators: List['Operator'] = []

    def get_value(self) -> str:
        return self.formula
    
    def validate_formula_format():
        """
        Validates that the input begins with an equals sign
        """
        pass

# Visitor software pattern for solving postfix evaluation
class FormulaElementVisitor(ABC):
    """Abstract visitor interface for formula elements"""
    
    @abstractmethod
    def visit_operator(self, operator: 'Operator') -> Any:
        pass
    
    @abstractmethod
    def visit_operand(self, operand: 'Operand') -> Any:
        pass

class FormulaElement(ABC):
    """Base class for all formula elements"""
    
    @abstractmethod
    def accept(self, visitor: FormulaElementVisitor) -> Any:
        pass
# TODO -> define the ArithmeticOperator class
class Operator(FormulaElement):
    """Represents mathematical operators in formulas"""
    
    def __init__(self, operator_type: str) -> None:
        self.type: str = operator_type

    def accept(self, visitor: FormulaElementVisitor) -> Any:
        return visitor.visit_operator(self)

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

# Generic postifxevaluation copied from claude -
class PostfixEvaluationVisitor(FormulaElementVisitor):
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet
        self.evaluation_stack = []
    
    def visit_operator(self, operator):
        # Pop necessary operands from stack
        right_operand = self.evaluation_stack.pop()
        left_operand = self.evaluation_stack.pop()
        
        # Perform operation and push result
        result = self._perform_operation(operator.type, left_operand, right_operand)
        self.evaluation_stack.append(result)
    
    def visit_operand(self, operand: Operand):
        value = operand.get_value(self.spreadsheet)
        self.evaluation_stack.append(value)

    # TODO claude has generated code for these functions but I have not copied for clarity first
    def _perform_operation(self, operator_type, left, right):
        # Implement operation logic
        pass
    
    def _evaluate_argument(self, argument):
        # Handle different argument types
        pass
    
    def _evaluate_function(self, function_name, arguments):
        # Implement function evaluation
        pass

class PostfixExpressionEvaluator:
    """Main class for evaluating postfix expressions using the visitor pattern"""
    
    def evaluate_postfix_expression(
        self, 
        postfix_expression: List[FormulaElement], 
        spreadsheet
    ) -> Union[int, float]:
        """
        Evaluate a postfix expression and return the result
        
        Args:
            postfix_expression: List of FormulaElement objects in postfix order
            spreadsheet: Context for accessing spreadsheet data
            
        Returns:
            Numeric result of the evaluation
            
        Raises:
            InvalidPostfixException: If the postfix expression is malformed
            EvaluationErrorException: If evaluation fails for any reason
        """
        # if not postfix_expression:
        #     raise InvalidPostfixException("Empty postfix expression")
        
        visitor = PostfixEvaluationVisitor(spreadsheet)
        
        # Process each element in postfix order
        for element in postfix_expression:
            element.accept(visitor)
        
        # Result should be the only item left on stack
        # if len(visitor.evaluation_stack) != 1:
        #     raise InvalidPostfixException(
        #         f"Invalid postfix expression: expected 1 result, got {len(visitor.evaluation_stack)}"
        #     )
        
        return visitor.evaluation_stack[0]

 # TODO
class FormulaParser:
    def __init__(self):
        pass

    def parse_tokens(self):
        pass
    
    def isOperand(self):
        pass

    def isOperator(self):
        pass

class Tokenizer:
    def __init__(self):
        pass

class PostfixConverter:
    def __init__(self):
        pass

class OperatorEvaluator:
    def __init__(self):
        pass
