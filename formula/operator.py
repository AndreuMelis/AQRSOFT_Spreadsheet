from formula.formula_element import FormulaElementVisitor, FormulaElement
from abc import ABC, abstractmethod
from typing import Any

class Operator(FormulaElement):
    @abstractmethod
    def get_symbol(self):
        """Return the operator symbol"""
        pass

    def accept(self, visitor: FormulaElementVisitor) -> Any:
        return visitor.visit_operator(self)
    
    @classmethod
    @abstractmethod
    def create_from_token(cls, token_value) -> 'Operator':
        """Factory method to create operator from token"""
        pass

class ArithmeticOperator(Operator):
    """Represents arithmetic operators like +, -, *, /"""
    
    def __init__(self, symbol: str) -> None:
        if symbol not in ['+', '-', '*', '/']:
            raise ValueError(f"Invalid arithmetic operator: {symbol}")
        self.symbol = symbol

    def get_symbol(self) -> str:
        return self.symbol
    
    @classmethod
    def create_from_token(cls, token_value) -> 'ArithmeticOperator':
        """Create ArithmeticOperator from token"""
        token_str = str(token_value)
        
        # Map token types/values to symbols
        token_map = {
            'PLUS': '+',
            'MINUS': '-',
            'TIMES': '*',
            'DIVIDE': '/',
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/'
        }
        
        if token_str in token_map:
            return cls(token_map[token_str])
        else:
            raise ValueError(f"Unknown arithmetic operator token: {token_value}")

class ParenthesisOperator(Operator):
    """Represents parenthesis operators ( and )"""
    
    def __init__(self, symbol: str) -> None:
        if symbol not in ['(', ')']:
            raise ValueError(f"Invalid parenthesis operator: {symbol}")
        self.symbol = symbol

    def get_symbol(self) -> str:
        return self.symbol
    
    @classmethod
    def create_from_token(cls, token_value) -> 'ParenthesisOperator':
        """Create ParenthesisOperator from token"""
        token_str = str(token_value)
        
        token_map = {
            'LPAREN': '(',
            'RPAREN': ')',
            '(': '(',
            ')': ')'
        }
        
        if token_str in token_map:
            return cls(token_map[token_str])
        else:
            raise ValueError(f"Unknown parenthesis operator token: {token_value}")

# NOTE: The top-level factory function create_operator_from_token has been removed
# as its logic is now integrated into the Parser class.