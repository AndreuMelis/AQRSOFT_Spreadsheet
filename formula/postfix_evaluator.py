from abc import ABC, abstractmethod
from exceptions import EvaluationErrorException, InvalidPostfixException


# Visitor software pattern for solving postfix evaluation
class FormulaElementVisitor(ABC):
    """Abstract visitor interface for formula elements"""
    @abstractmethod
    def visit_operator(self, operator):
        pass

    @abstractmethod
    def visit_operand(self, operand):
        pass

class FormulaElement(ABC):
    """Base class for all formula elements"""
    @abstractmethod
    def accept(self, visitor: FormulaElementVisitor):
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
