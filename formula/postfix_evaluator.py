from abc import ABC, abstractmethod
from typing import List, Union, Any

from exceptions import EvaluationErrorException, InvalidPostfixException
from formula.operand import Operand
from formula.operator import Operator
from formula.function import Function, FunctionArgument


class FormulaElementVisitor(ABC):
    """Visitor interface for formula elements in a postfix expression."""
    
    @abstractmethod
    def visit_operand(self, operand: Operand) -> None:
        pass

    @abstractmethod
    def visit_operator(self, operator: Operator) -> None:
        pass

    @abstractmethod
    def visit_function(self, function: Function) -> None:
        pass

class FormulaElement(ABC):
    """Base class for all formula elements"""
    @abstractmethod
    def accept(self, visitor: FormulaElementVisitor) -> Any:
        pass

# Generic postifxevaluation copied from claude -
class PostfixEvaluationVisitor(FormulaElementVisitor):
    """
    Evaluates a postfix (RPN) expression by visiting each node
    and maintaining an evaluation stack of plain numbers.
    """
     
    def __init__(self):
        self.evaluation_stack: List[Union[int, float]] = []
    
    def visit_operator(self, operator: Operator):
        if len(self.evaluation_stack) < 2:
            raise InvalidPostfixException(
                f"Not enough operands for operator '{operator.type}'"
            )
        right = self.evaluation_stack.pop()
        left = self.evaluation_stack.pop()
        result = self._perform_operation(operator.type, left, right)
        self.evaluation_stack.append(result)
    
    def visit_operand(self, operand: Operand):
        """Process an operand by pushing its value to the stack"""
        value = operand.get_value()
        self.evaluation_stack.append(value)
    
    def visit_function(self, function_element: FormulaElement):
        """Process a function by evaluating its arguments and calling the function"""
        try:
            # Evaluate all arguments
            argument_values = []
            for arg in function_element.arguments:
                if isinstance(arg, FunctionArgument):
                    # Use your FunctionArgument.get_value method
                    value = arg.get_value(function_element.spreadsheet)
                    # Handle both single values and lists (for ranges)
                    if isinstance(value, list):
                        argument_values.extend(value)
                    else:
                        argument_values.append(value)
                else:
                    # Fallback for other argument types
                    argument_values.append(arg)
            
            # Evaluate the function and push result
            result = self._evaluate_function(function_element.function_instance, argument_values)
            self.evaluation_stack.append(result)
        except Exception as e:
            raise EvaluationErrorException(f"Function evaluation failed: {str(e)}")

    # TODO claude has generated code for these functions but I have not copied for clarity first
    def _perform_operation(self, operator_type: str, left: Union[int, float], right: Union[int, float]) -> Union[int, float]:
        """Execute a binary arithmetic operation"""
        if operator_type == '+':
            return left + right
        elif operator_type == '-':
            return left - right
        elif operator_type == '*':
            return left * right
        elif operator_type == '/':
            if right == 0:
                raise EvaluationErrorException("Division by zero")
            return left / right
        else:
            raise EvaluationErrorException(f"Unsupported operator: {operator_type}")
    
    def _evaluate_argument(self, argument: Any) -> Union[int, float]:
        """
        Handle different argument types for function evaluation
        This method is for future extensibility when handling functions
        """
        if isinstance(argument, (int, float)):
            return argument
        elif isinstance(argument, Operand):
            return argument.get_value()
        else:
            raise EvaluationErrorException(f"Unknown argument type: {type(argument)}")
    
    def _evaluate_function(self, function_instance: Function, arguments: List[Union[int, float]]) -> Union[int, float]:
        """
        Evaluate functions using your Function class hierarchy
        This integrates with your existing function.py architecture
        """
        try:
            # Use your Function.evaluate method
            return function_instance.evaluate(arguments)
        except Exception as e:
            raise EvaluationErrorException(f"Function evaluation failed: {str(e)}")

class PostfixExpressionEvaluator:
    """Main class for evaluating postfix expressions using the visitor pattern"""
    
    def evaluate_postfix_expression(
        self, 
        postfix_expression: List[FormulaElement], 
    ) -> Union[int, float]:
        """
        Evaluate a postfix expression and return the result
        
        Args:
            postfix_expression: List of FormulaElement objects in postfix order            
        Returns:
            Numeric result of the evaluation
            
        Raises:
            InvalidPostfixException: If the postfix expression is malformed
            EvaluationErrorException: If evaluation fails for any reason
        """
        if not postfix_expression:
            raise InvalidPostfixException("Empty postfix expression")
        
        visitor = PostfixEvaluationVisitor()
        
        # Process each element in postfix order
        for element in postfix_expression:
            element.accept(visitor)
        
        # Result should be the only item left on stack
        if len(visitor.evaluation_stack) != 1:
            raise InvalidPostfixException(
                f"Invalid postfix expression: expected 1 result, got {len(visitor.evaluation_stack)}"
            )
        
        return visitor.evaluation_stack[0]