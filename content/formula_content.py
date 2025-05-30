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
from spreadsheet.dependency_manager import DependencyManager

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

        # Step 1: Tokenize into raw strings (e.g., ['A1', '+', '3'])
        tokens = self.tokenize(raw_expression)

        # Step 2: Parse into typed tokens (Operator, Operand, Reference, etc.)
        typed_tokens = self.parse_tokens(tokens, spreadsheet)

        # Step 3: Check for circular dependencies — we pass spreadsheet to trace references
        self.check_circular_dependencies(spreadsheet)

        # Step 4: Convert to postfix for evaluation
        postfix_tokens = self.convert_to_postfix(typed_tokens)

        # Step 5: Evaluate postfix expression — now we resolve references using the spreadsheet
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
        Extracts the current cell and all referenced cells from the formula,
        and checks for circular dependencies.
        """
        # STEP 1 — Get the name of the current cell this formula is part of
        current_cell = spreadsheet.get_cell_name(self)  # <-- You'll need to implement this method

        # STEP 2 — Tokenize the formula and extract references
        raw_expression = self.formula[1:]  # Remove the '='
        tokens = self.tokenize(raw_expression)  # Returns list like ['A1', '+', 'B2']

        # STEP 3 — Identify referenced cells (tokens that look like 'A1', 'C3', etc.)
        referenced_cells = {
            token.upper()
            for token in tokens
            if spreadsheet.is_valid_cell_reference(token)
        }

        # STEP 4 — Use DependencyManager to detect cycles
        dependency_manager = spreadsheet.get_dependency_manager()  # Singleton or instance passed into spreadsheet
        dependency_manager.check_circular_dependencies(current_cell, referenced_cells)

        # STEP 5 — If all is good, update the graph
        dependency_manager.update_dependencies(current_cell, referenced_cells)

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

