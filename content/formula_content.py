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
from formula.formula_element import FormulaElement
from spreadsheet.spreadsheet import Spreadsheet
from formula.operand import CellOperand, FunctionOperand
from formula.function import FunctionArgument, CellArgument, CellRangeArgument, FunctionArgumentWrapper
from typing import Set
import re

class FormulaContent(CellContent):
    def __init__(self, formula: str) -> None:
        super().__init__()
        self.formula: str = formula
        self.elements: List[FormulaElement] = []
        self.tokenizer = Tokenizer()
        self.parser: Optional[Parser] = None
        self.postfix_converter: PostfixConverter = PostfixConverter()
        self.postfix_evaluator: PostfixExpressionEvaluator = PostfixExpressionEvaluator()
        
        # Simple caching: store the computed value
        self._computed_value: Optional[float] = None

        self._parsed_tokens = None

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

        raw_expression = str(self.formula)[1:].replace(',', ';')

        # Tokenize into raw strings 
        tokens = self.tokenizer.tokenize(raw_expression)

        # Parse into typed tokens 
        self.parser = Parser(tokens)
        self.elements = self.parser.parse_tokens(spreadsheet)

        # Check for circular dependencies
        self.check_circular_dependencies(spreadsheet, current_cell_name)

        # Convert to postfix for evaluation
        self.postfix_converter = PostfixConverter()
        postfix_tokens = self.postfix_converter.convert_to_postfix(self.elements)

        # Evaluate postfix expression
        result = self.postfix_evaluator.evaluate_postfix_expression(postfix_tokens)

        return result

    def invalidate_value(self):
        """Mark the stored value as invalid, forcing recomputation on next access"""
        self._computed_value = None
        self._parsed_tokens = None

    def has_computed_value(self) -> bool:
        """Check if this formula has a stored computed value"""
        return self._computed_value is not None

    def validate_formula_format(self) -> bool:
        """Validates that the formula begins with an equals sign."""
        return self.formula.startswith("=")

    def check_circular_dependencies(self, spreadsheet: Spreadsheet, current_cell_name: str = None):
        """Uses typed tokens from parser instead of manual string parsing."""
        if current_cell_name is None:
            try:
                current_cell = spreadsheet.get_cell_name(self)
            except ValueError:
                raise ValueError("Cannot determine current cell name for circular dependency check")
        else:
            current_cell = current_cell_name

        # Parse tokens if not already cached
        if self._parsed_tokens is None:
            raw_expression = str(self.formula)[1:].replace(',', ';')
            tokens = self.tokenizer.tokenize(raw_expression)
            self.parser = Parser(tokens)
            self._parsed_tokens = self.parser.parse_tokens(spreadsheet)

        # Use existing dependency checking logic
        dependency_manager = spreadsheet.dep_manager
        # Get referenced cells using typed tokens
        referenced_cells = dependency_manager.get_referenced_cells_from_tokens(self._parsed_tokens)
        dependency_manager.check_circular_dependencies(current_cell, referenced_cells)
        dependency_manager.update_dependencies(current_cell, referenced_cells)

    def get_text(self) -> str:
        """Returns the formula as a string exactly as stored."""
        return str(self.formula)
    
    def __repr__(self):
        computed_status = "computed" if self._computed_value is not None else "not computed"
        return f"FormulaContent(formula='{self.formula}', {computed_status})"