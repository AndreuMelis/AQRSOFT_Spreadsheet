from cell_content import CellContent
from abc import ABC, abstractmethod
from typing import Any, List, Union, Optional

# falta tokenizer, parser, evaluate function, perform operation...

# Incomplete, just for clarity
class FormulaContent(CellContent):
    def __init__(self, formula: str) -> None:
        super().__init__()
        self.formula: str = formula
        self.operands: List['Operand'] = []
        self.operators: List['Operator'] = []

    def get_value(self) -> str:
        return self.formula

# Function argument types
class FunctionArgument(ABC):
    """Base class for function arguments"""
    pass

class CellArgument(FunctionArgument):
    def __init__(self, cell_reference: str) -> None:
        self.reference: str = cell_reference

class CellRangeArgument(FunctionArgument):
    def __init__(self, range_reference: str) -> None:
        self.range_reference: str = range_reference  # e.g., "A1:C5"

class NumericArgument(FunctionArgument):
    def __init__(self, value: Union[int, float]) -> None:
        self.value: Union[int, float] = value


# Visitor software pattern for solving postfix evaluation
class FormulaElementVisitor(ABC):
    """Abstract visitor interface for formula elements"""
    
    @abstractmethod
    def visit_operator(self, operator: 'Operator') -> Any:
        pass
    
    @abstractmethod
    def visit_numeric_operand(self, numeric: 'NumericOperand') -> Any:
        pass
    
    @abstractmethod
    def visit_cell_operand(self, cell: 'CellOperand') -> Any:
        pass
    
    @abstractmethod
    def visit_function_operand(self, function: 'Function') -> Any:
        pass

class FormulaElement(ABC):
    """Base class for all formula elements"""
    
    @abstractmethod
    def accept(self, visitor: FormulaElementVisitor) -> Any:
        pass

class Operator(FormulaElement):
    """Represents mathematical operators in formulas"""
    
    def __init__(self, operator_type: str) -> None:
        self.type: str = operator_type

    def accept(self, visitor: FormulaElementVisitor) -> Any:
        return visitor.visit_operator(self)

class Operand(FormulaElement):
    """Base class for all operands"""
    pass

class NumericOperand(Operand):
    """Represents numeric literal values"""
    
    def __init__(self, value: Union[int, float]) -> None:
        self.value: Union[int, float] = value

    def accept(self, visitor: FormulaElementVisitor) -> Any:
        return visitor.visit_numeric_operand(self)

class CellOperand(Operand):
    """Represents cell references like A1, B2"""
    
    def __init__(self, reference: str) -> None:
        self.reference: str = reference

    def accept(self, visitor: FormulaElementVisitor) -> Any:
        return visitor.visit_cell_operand(self)
    
class Function(Operand):
    """Represents spreadsheet functions like SUM, MIN, MAX"""
    
    def __init__(self, name: str, arguments: List[FunctionArgument]) -> None:
        self.name: str = name
        self.arguments: List[FunctionArgument] = arguments

    def accept(self, visitor: FormulaElementVisitor) -> Any:
        return visitor.visit_function_operand(self)

# Generic postifxevaluation copied from claude -
class PostfixEvaluationVisitor(FormulaElementVisitor):
    def __init__(self, spreadsheet_context):
        self.spreadsheet_context = spreadsheet_context
        self.evaluation_stack = []
    
    def visit_operator(self, operator):
        # Pop necessary operands from stack
        right_operand = self.evaluation_stack.pop()
        left_operand = self.evaluation_stack.pop()
        
        # Perform operation and push result
        result = self._perform_operation(operator.type, left_operand, right_operand)
        self.evaluation_stack.append(result)
    
    def visit_numeric_operand(self, numeric):
        # Simply push numeric value to stack
        self.evaluation_stack.append(numeric.value)
    
    def visit_cell_operand(self, cell):
        # Resolve cell reference and push value to stack
        cell_value = self.spreadsheet_context.get_cell_value(cell.reference)
        self.evaluation_stack.append(cell_value)
    
    def visit_function_operand(self, function):
        # Evaluate function arguments
        arg_values = []
        for arg in function.arguments:
            arg_value = self._evaluate_argument(arg)
            arg_values.append(arg_value)
        
        # Perform function and push result
        result = self._evaluate_function(function.name, arg_values)
        self.evaluation_stack.append(result)
    
    # claude has generated code for these functions but I have not copied for clarity first
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
        spreadsheet_context
    ) -> Union[int, float]:
        """
        Evaluate a postfix expression and return the result
        
        Args:
            postfix_expression: List of FormulaElement objects in postfix order
            spreadsheet_context: Context for accessing spreadsheet data
            
        Returns:
            Numeric result of the evaluation
            
        Raises:
            InvalidPostfixException: If the postfix expression is malformed
            EvaluationErrorException: If evaluation fails for any reason
        """
        # if not postfix_expression:
        #     raise InvalidPostfixException("Empty postfix expression")
        
        visitor = PostfixEvaluationVisitor(spreadsheet_context)
        
        # Process each element in postfix order
        for element in postfix_expression:
            element.accept(visitor)
        
        # Result should be the only item left on stack
        # if len(visitor.evaluation_stack) != 1:
        #     raise InvalidPostfixException(
        #         f"Invalid postfix expression: expected 1 result, got {len(visitor.evaluation_stack)}"
        #     )
        
        return visitor.evaluation_stack[0]