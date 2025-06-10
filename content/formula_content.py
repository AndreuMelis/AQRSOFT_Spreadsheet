from content.cell_content import CellContent
from typing import List, Optional
from abc import ABC, abstractmethod
from formula.tokenizer   import Tokenizer
from formula.parser      import Parser
from formula.postfix_converter import PostfixConverter
from formula.postfix_evaluator   import PostfixExpressionEvaluator
from formula.operand import Operand
from formula.operator import Operator
from formula.parser import Parser
from formula.postfix_converter import PostfixConverter
from spreadsheet.spreadsheet import Spreadsheet
import re

class FormulaContent(CellContent):
    def __init__(self, formula: str) -> None:
        super().__init__()
        self.formula: str = formula
        self.operands: List['Operand'] = []
        self.operators: List['Operator'] = []
        self.tokenizer = Tokenizer()
        self.parser: Optional[Parser] = None
        self.postfix_converter: PostfixConverter = PostfixConverter()
        self.postfix_evaluator: PostfixExpressionEvaluator = PostfixExpressionEvaluator()
        
        # Simple caching: store the computed value
        self._computed_value: Optional[float] = None

    def get_value(self, spreadsheet: Optional[Spreadsheet] = None, current_cell_name: str = None) -> float:
        # If we already have a computed value, return it
        if self._computed_value is not None:
            return self._computed_value
            
        # Otherwise, compute and store the value
        self._computed_value = self._compute_value(spreadsheet, current_cell_name)
        return self._computed_value

    def _compute_value(self, spreadsheet: Spreadsheet, current_cell_name: str = None) -> float:
        """Internal method that actually computes the formula value"""
        if not self.validate_formula_format():
            raise ValueError("Invalid formula format: must start with '='")

        # Don't modify the original formula - create a copy for processing
        raw_expression = str(self.formula)[1:].replace(',', ';')

        # Step 1: Tokenize into raw strings (e.g., ['A1', '+', '3'])
        tokens = self.tokenizer.tokenize(raw_expression)

        # Step 2: CHECK CIRCULAR DEPENDENCIES FIRST, before creating objects
        self.check_circular_dependencies(spreadsheet, current_cell_name)

        # Step 3: Parse into typed tokens (Operator, Operand, Reference, etc.)
        self.parser = Parser(tokens)
        typed_tokens = self.parser.parse_tokens(spreadsheet)

        # Step 4: Convert to postfix for evaluation
        self.postfix_converter = PostfixConverter()
        postfix_tokens = self.postfix_converter.convert_to_postfix(typed_tokens)

        # Step 5: Evaluate postfix expression
        result = self.postfix_evaluator.evaluate_postfix_expression(postfix_tokens)

        return result

    def invalidate_value(self):
        """Mark the stored value as invalid, forcing recomputation on next access"""
        self._computed_value = None

    def has_computed_value(self) -> bool:
        """Check if this formula has a stored computed value"""
        return self._computed_value is not None

    def validate_formula_format(self) -> bool:
        """
        Validates that the formula begins with an equals sign.
        """
        return self.formula.startswith("=")

    def check_circular_dependencies(self, spreadsheet: Spreadsheet, current_cell_name: str = None):
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

        # Identify referenced cells (only tokens whose kind is 'RANGE' or 'CELL')
        referenced_cells = set(self.get_referenced_cells())

        # STEP 4 — Use DependencyManager to detect cycles
        dependency_manager = spreadsheet.dep_manager
        dependency_manager.check_circular_dependencies(current_cell, referenced_cells)

        # STEP 5 — If all is good, update the graph
        dependency_manager.update_dependencies(current_cell, referenced_cells)

    def get_referenced_cells(self) -> list:
        """
        Returns a list of all cell names referenced in the formula,
        expanding ranges like A6:A10 to ['A6', 'A7', 'A8', 'A9', 'A10'].
        """
        if not self.validate_formula_format():
            return []

        expr = self.formula[1:].replace(',', ';')
        refs = set()

        # Expand ranges like A6:A10
        for match in re.finditer(r'([A-Z]+)(\d+):([A-Z]+)(\d+)', expr):
            col1, row1, col2, row2 = match.groups()
            if col1 == col2:
                for row in range(int(row1), int(row2) + 1):
                    refs.add(f"{col1}{row}")
            # (If you want to support multi-column ranges, add logic here)

        # Find all single cell references not part of a range
        for match in re.finditer(r'([A-Z]+)(\d+)', expr):
            cell = match.group(0)
            refs.add(cell)

        return list(refs)

    def get_text(self) -> str:
        """
        Returns the formula as a string exactly as stored.
        """
        return str(self.formula)
    
    def __repr__(self):
        computed_status = "computed" if self._computed_value is not None else "not computed"
        return f"FormulaContent(formula='{self.formula}', {computed_status})"