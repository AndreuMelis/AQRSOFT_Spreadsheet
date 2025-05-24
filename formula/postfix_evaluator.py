from abc import ABC, abstractmethod
from exceptions import EvaluationErrorException, InvalidPostfixException

# Define the visitor & evaluator here:
class FormulaElementVisitor(ABC):
    @abstractmethod
    def visit_operator(self, operator):
        pass

    @abstractmethod
    def visit_operand(self, operand):
        pass

class PostfixEvaluationVisitor(FormulaElementVisitor):
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet
        self.evaluation_stack = []

    def visit_operator(self, operator):
        # TODO: Pop operands, apply operator, push result
        pass

    def visit_operand(self, operand):
        # TODO: Retrieve operand value and push onto stack
        pass

class PostfixExpressionEvaluator:
    def evaluate_postfix_expression(self, postfix_expression, spreadsheet):
        """
        Evaluate a postfix list of FormulaElement, returning numeric result.
        """
        # TODO: Implement visitor pattern evaluation
        pass