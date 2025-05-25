from content.cell_content import CellContent
from typing import List
from abc import ABC, abstractmethod
from formula.tokenizer   import Tokenizer
from formula.parser      import Parser
from formula.postfix_converter import InfixToPostfixConverter
from formula.postfix_evaluator   import PostfixExpressionEvaluator
from formula.operand import Operand
from formula.operator import Operator

# TODO -> define FormulaContent completely, tokenizer, parser, evaluate function, perform operation...
# Incomplete, just for clarity
# May substitute FormulaController defined in the documents
class FormulaContent(CellContent):
    def __init__(self, formula: str) -> None:
        super().__init__()
        self.formula: str = formula
        self.operands: List['Operand'] = []
        self.operators: List['Operator'] = []

    def get_value(self, spreadsheet=None) -> float:
        if not self.validate_formula_format():
            raise ValueError("Invalid formula format: must start with '='")

        raw_expression = self.formula[1:]
        tokens = self.tokenize(raw_expression)
        postfix_tokens = self.convert_to_postfix(tokens)
        result = self.evaluate_postfix(postfix_tokens, spreadsheet)
        return result

    def validate_formula_format(self) -> bool:
        """
        Validates that the formula begins with an equals sign.
        """
        return self.formula.startswith("=")

    def tokenize(self, expression: str):
        """
        Tokenizes the input expression using the Tokenizer class.
        """
        return Tokenizer.tokenize(expression)

    def convert_to_postfix(self, tokens):
        """
        Converts infix tokens to postfix using the InfixToPostfixConverter.
        """
        converter = InfixToPostfixConverter(tokens)
        return converter.convert()

    def evaluate_postfix(self, postfix_tokens, spreadsheet):
        """
        Evaluates the postfix expression using PostfixExpressionEvaluator.
        """
        evaluator = PostfixExpressionEvaluator(postfix_tokens, spreadsheet)
        return evaluator.evaluate_postfix_expression()

    def __repr__(self):
        return f"FormulaContent(formula='{self.formula}')"

