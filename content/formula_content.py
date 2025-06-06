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
from spreadsheet.dependency_manager import DependencyManager
from spreadsheet.spreadsheet import Spreadsheet
from spreadsheet.dependency_manager import DependencyManager

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
        result = self.evaluate_postfix(postfix_tokens)

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
        # ← One‐line change here: call tokenize on an instance, not on the class
        return Tokenizer().tokenize(expression)
    
    def parse_tokens(self, tokens: list, spreadsheet: Spreadsheet):
        """
        Validates the syntax of tokenized formula component.
        """
        parser = Parser(tokens)
        return parser.parse_tokens(spreadsheet)


    def check_circular_dependencies(self, spreadsheet: Spreadsheet):
        """
        Extracts the current cell and all referenced cells from the formula,
        and checks for circular dependencies.
        """
        # STEP 1 — Get the name of the current cell this formula is part of
        current_cell = spreadsheet.get_cell_name(self)

        # STEP 2 — Tokenize the formula and extract references
        raw_expression = self.formula[1:]  # Remove the '='
        tokens = self.tokenize(raw_expression)  # List of (kind, value) pairs

        # STEP 3 — Identify referenced cells (only tokens whose kind is 'CELL')
        referenced_cells = {
            value.upper()
            for (kind, value) in tokens
            if kind == 'CELL' and spreadsheet.is_valid_cell_reference(value)
        }

        # STEP 4 — Use DependencyManager to detect cycles
        dependency_manager = spreadsheet.get_dependency_manager()
        dependency_manager.check_circular_dependencies(current_cell, referenced_cells)

        # STEP 5 — If all is good, update the graph
        dependency_manager.update_dependencies(current_cell, referenced_cells)


    def convert_to_postfix(self, tokens):
        """
        Converts infix tokens to postfix using the PostfixConverter.
        """
        converter = PostfixConverter()            # ← no arguments here
        return converter.convert_to_postfix(tokens)


    def evaluate_postfix(self, postfix_tokens):
        """
        Evaluates the postfix expression using PostfixExpressionEvaluator.
        """
        evaluator = PostfixExpressionEvaluator()                      # ← no arguments here
        return evaluator.evaluate_postfix_expression(postfix_tokens)  # ← pass tokens into the method


    def __repr__(self):
        return f"FormulaContent(formula='{self.formula}')"
