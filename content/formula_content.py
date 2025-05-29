from content.cell_content import CellContent
from typing import List
from abc import ABC, abstractmethod
from formula.tokenizer   import Tokenizer
from formula.parser      import Parser
from formula.postfix_converter import PostfixConverter
from formula.postfix_evaluator   import PostfixExpressionEvaluator
from formula.operand import Operand
from formula.operator import Operator
from formula.parser import Parser
from formula.postfix_converter import PostfixConverter
from formula.dependency_manager import DependencyManager
from spreadsheet.spreadsheet import Spreadsheet

# TODO -> define FormulaContent completely, tokenizer, parser, evaluate function, perform operation...
# Incomplete, just for clarity
# May substitute FormulaController defined in the documents
class FormulaContent(CellContent):
    def __init__(self, formula: str) -> None:
        super().__init__()
        self.formula: str = formula
        self.operands: List['Operand'] = []
        self.operators: List['Operator'] = []

    def get_value(self, spreadsheet: Spreadsheet) -> float:
        if not self.validate_formula_format():
            raise ValueError("Invalid formula format: must start with '='")

        raw_expression = self.formula[1:]
        # create a list of tokens from the formula string
        """
        SEGONS EL NOSTRE DISSENY CREC QUE LA LLISTA DE TOKENS HAN DE SER OPERANDS I OPERATORS, 
        NO STRINGS, I SEGONS EL JUAN CARLOS SI HO FEM AIXÍ NO NECESSITAREM L'SPREADSHEET PER
        RESOLDRE CAP REFERÈNCIA. LA CONVERSIÓ A OPERANDS I OPERATORS HA DE SER DINS PARSER, 
        SEGONS EL NOSTRE DISSENY

        """
        tokens = self.tokenize(raw_expression)
        # validates the syntax of a tokenized formula components
        tokens = self.parse_tokens(tokens, spreadsheet)
        # TODO -> where to place check_circular_dependencies so it has access to current and referenced cells
        # the spreadsheet is passed to get_value, it can be used
        self.check_circular_dependencies(spreadsheet)
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
    
    def parse_tokens(self, tokens: list):
        """
        Validates the syntax of tokenized formula component.
        """
        parser = Parser(tokens)
        tokens = parser.parse_tokens()
        return 

    def check_circular_dependencies(self, spreadsheet: Spreadsheet):
        """
        Validates the syntax of tokenized formula component.
        """
        pass
        # TODO -> from spreadsheet and formula attribute extract the current cell and referenced cells
        # DependencyManager.check_circular_dependencies()

    def convert_to_postfix(self, tokens):
        """
        Converts infix tokens to postfix using the InfixToPostfixConverter.
        """
        converter = PostfixConverter(tokens)
        return converter.convert_to_postfix()

    def evaluate_postfix(self, postfix_tokens):
        """
        Evaluates the postfix expression using PostfixExpressionEvaluator.
        """
        evaluator = PostfixExpressionEvaluator(postfix_tokens)
        return evaluator.evaluate_postfix_expression()

    def __repr__(self):
        return f"FormulaContent(formula='{self.formula}')"

