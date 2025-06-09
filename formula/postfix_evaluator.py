# formula/postfix_evaluator.py

from .formula_element import FormulaElementVisitor, FormulaElement
from .operand import Operand, CellOperand, FunctionOperand, NumericOperand
from .operator import Operator
from .function import Function, FunctionArgument
from exceptions import InvalidPostfixException, EvaluationErrorException
from typing import List, Union

class PostfixEvaluationVisitor(FormulaElementVisitor):
    """
    Implementation of FormulaElementVisitor that evaluates a postfix expression.
    Maintains an internal stack of numeric values.
    """
    def __init__(self):
        self.evaluation_stack: List[Union[int, float]] = []

    def visit_operand(self, operand: Operand):
        """Push the operand's value onto the stack."""
        value = operand.get_value()
        self.evaluation_stack.append(value)

    def visit_operator(self, operator: Operator):
        """Pop two values, apply operator, push result."""
        if len(self.evaluation_stack) < 2:
            raise InvalidPostfixException(
                f"Not enough operands for operator '{operator.get_symbol()}'"
            )
        right = self.evaluation_stack.pop()
        left = self.evaluation_stack.pop()
        result = self._perform_operation(operator.get_symbol(), left, right)
        self.evaluation_stack.append(result)

    def _perform_operation(
        self,
        operator_symbol: str,
        left: Union[int, float],
        right: Union[int, float]
    ) -> Union[int, float]:
        if operator_symbol == '+':
            return left + right
        elif operator_symbol == '-':
            return left - right
        elif operator_symbol == '*':
            return left * right
        elif operator_symbol == '/':
            if right == 0:
                raise EvaluationErrorException("Division by zero")
            return left / right
        else:
            raise EvaluationErrorException(f"Unsupported operator: {operator_symbol}")

class PostfixExpressionEvaluator:
    """Main class to evaluate a list of FormulaElement in postfix order."""
    def __init__(self):
        pass
    def evaluate_postfix_expression(
        self,
        postfix_expression: List[FormulaElement],
    ) -> Union[int, float]:
        if not postfix_expression:
            raise InvalidPostfixException("Empty postfix expression")
        visitor = PostfixEvaluationVisitor()
        for element in postfix_expression:
            element.accept(visitor)
        if len(visitor.evaluation_stack) != 1:
            raise InvalidPostfixException(
                f"Invalid postfix expression: expected 1 result, got {len(visitor.evaluation_stack)}"
            )
        return visitor.evaluation_stack[0]
