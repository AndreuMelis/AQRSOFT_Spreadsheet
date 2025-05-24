from content.cell_content import CellContent
from abc import ABC, abstractmethod
from formula.tokenizer   import Tokenizer
from formula.parser      import Parser
from AQRSOFT_Spreadsheet.formula.postfix_converter import InfixToPostfixConverter
from formula.postfix_evaluator   import PostfixExpressionEvaluator

# TODO -> define FormulaContent completely, tokenizer, parser, evaluate function, perform operation...
"""
Main idea: el Evaluate postfix expression visitor diferencia entre operand i operator,
per tant, utilitzant inheritance d'operand, puc obtenir el valor de cada subclasse d'operand
amb el corresponent get_value concret
"""
# Incomplete, just for clarity
# May substitute FormulaController defined in the documents
class FormulaContent(CellContent):
    def __init__(self, formula: str) -> None:
        super().__init__()
        self.formula: str = formula
        self.operands: List['Operand'] = []
        self.operators: List['Operator'] = []

    def get_value(self) -> str:
        return self.formula
    
    def validate_formula_format():
        """
        Validates that the input begins with an equals sign
        """
        pass
