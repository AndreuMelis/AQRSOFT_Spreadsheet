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

    def get_value(self, spreadsheet: Spreadsheet, current_cell_name: str = None) -> float:
        if not self.validate_formula_format():
            raise ValueError("Invalid formula format: must start with '='")

        # Don't modify the original formula - create a copy for processing
        raw_expression = str(self.formula)[1:].replace(',', ';')

        # Step 1: Tokenize into raw strings (e.g., ['A1', '+', '3'])
        tokens = self.tokenize(raw_expression)

        # Step 2: CHECK CIRCULAR DEPENDENCIES FIRST, before creating objects
        self.check_circular_dependencies(spreadsheet, tokens, current_cell_name)

        # Step 3: Parse into typed tokens (Operator, Operand, Reference, etc.)
        typed_tokens = self.parse_tokens(tokens, spreadsheet)

        # Step 4: Convert to postfix for evaluation
        postfix_tokens = self.convert_to_postfix(typed_tokens)

        # Step 5: Evaluate postfix expression
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
        # ← One‐line change here: call tokenize on an instance, not on the class
        return Tokenizer().tokenize(expression)
    
    def parse_tokens(self, tokens: list, spreadsheet: Spreadsheet):
        """
        Validates the syntax of tokenized formula component.
        """
        parser = Parser(tokens)
        return parser.parse_tokens(spreadsheet)


    def check_circular_dependencies(self, spreadsheet: Spreadsheet, tokens: list, current_cell_name: str = None):
        """
        Extracts the current cell and all referenced cells from the formula,
        and checks for circular dependencies.
        """
        # STEP 1 — Get the name of the current cell this formula is part of
        if current_cell_name is None:
            try:
                current_cell = spreadsheet.get_cell_name(self)
            except ValueError:
                # If we can't find the cell (it hasn't been added yet), we need the cell name
                # This happens when setting a cell's content - we need to pass the cell name
                raise ValueError("Cannot determine current cell name for circular dependency check")
        else:
            current_cell = current_cell_name

        # Identify referenced cells (only tokens whose kind is 'CELL')
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
        converter = PostfixConverter()            
        return converter.convert_to_postfix(tokens)


    def evaluate_postfix(self, postfix_tokens, spreadsheet):
        evaluator = PostfixExpressionEvaluator(spreadsheet)
        return evaluator.evaluate_postfix_expression(postfix_tokens)


    def get_text(self) -> str:
        """
        Returns the formula as a string exactly as stored.
        """
        return str(self.formula)
    
    
    def __repr__(self):
        return f"FormulaContent(formula='{self.formula}')"