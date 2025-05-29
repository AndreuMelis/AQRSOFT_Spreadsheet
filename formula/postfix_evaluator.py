from abc import ABC, abstractmethod
from exceptions import EvaluationErrorException, InvalidPostfixException
from typing import List, Union, Any
from formula.operand import Operand
from formula.operator import Operator
# Visitor software pattern for solving postfix evaluation
"""
Main idea: el Evaluate postfix expression visitor diferencia entre operand i operator,
per tant, utilitzant inheritance d'operand, puc obtenir el valor de cada subclasse d'operand
amb el corresponent get_value concret
"""
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

# Generic postifxevaluation copied from claude -
class PostfixEvaluationVisitor(FormulaElementVisitor):
    def __init__(self):
        self.evaluation_stack: List[Union[int, float]] = []
    
    def visit_operator(self, operator: Operator):
        # Pop necessary operands from stack
        right_operand = self.evaluation_stack.pop()
        left_operand = self.evaluation_stack.pop()
        
        # Perform operation and push result
        result = self._perform_operation(operator.type, left_operand, right_operand)
        self.evaluation_stack.append(result)
    
    def visit_operand(self, operand: Operand):
        value = operand.get_value()
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
