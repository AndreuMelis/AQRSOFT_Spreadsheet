import re
from exceptions import SyntaxErrorException
from spreadsheet.spreadsheet import Spreadsheet
from typing import Union, List, Tuple

# Import concrete classes
from formula.operand import Operand, NumericOperand, CellOperand, FunctionOperand
from formula.operator import Operator, ArithmeticOperator, ParenthesisOperator
from formula.function import FunctionArgument, CellArgument, CellRangeArgument, NumericArgument, FunctionArgumentWrapper

class Parser:
    """
    Simplified parser that converts tokens into operands and operators.
    Function arguments are handled as FunctionArgument objects, not operands.
    """
    
    def __init__(self, tokens: List[Tuple[str, str]]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Union[Tuple[str, str], None]:
        """Get current token without advancing"""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self) -> Union[Tuple[str, str], None]:
        """Get current token and advance position"""
        token = self.current_token()
        if token:
            self.pos += 1
        return token

    def parse_tokens(self, spreadsheet: Spreadsheet) -> List[Union[Operand, Operator]]:
        """Parse tokens into operands and operators"""
        if not self.tokens:
            raise SyntaxErrorException("No tokens to parse")
        
        self.pos = 0
        result = []
        
        while self.pos < len(self.tokens):
            element = self._parse_element(spreadsheet)
            if element:
                result.append(element)
        
        if not result:
            raise SyntaxErrorException("Formula is empty or invalid")
            
        return result
    
    def _parse_element(self, spreadsheet: Spreadsheet) -> Union[Operand, Operator, None]:
        """Parse a single element (operand or operator)"""
        token = self.current_token()
        if not token:
            return None
            
        token_type, token_value = token
        
        # Try to create operand first
        if token_type == 'NUMBER':
            self.advance()
            return NumericOperand.create_from_token(token_value)
            
        elif token_type == 'CELL':
            self.advance()
            return CellOperand.create_from_token(token_value, spreadsheet)
            
        elif token_type == 'FUNC':
            return self._parse_function(token_value, spreadsheet)
            
        # Try to create operator
        elif token_type in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE'] or token_value in ['+', '-', '*', '/']:
            self.advance()
            return ArithmeticOperator.create_from_token(token_value)
            
        elif token_type in ['LPAREN', 'RPAREN'] or token_value in ['(', ')']:
            self.advance()
            return ParenthesisOperator.create_from_token(token_value)
            
        else:
            raise SyntaxErrorException(f"Unknown token: {token_type} '{token_value}'")

    def _parse_function(self, func_name: str, spreadsheet: Spreadsheet) -> FunctionOperand:
        """Parse a function with its arguments"""
        self.advance()  # consume function name
        
        # Create function operand
        func_operand = FunctionOperand.create_from_token(func_name, spreadsheet)
        
        # Expect opening parenthesis
        token = self.current_token()
        if not token or token[0] != 'LPAREN':
            raise SyntaxErrorException(f"Expected '(' after function {func_name}")
        self.advance()  # consume '('
        
        # Parse arguments
        arguments = []
        if self.current_token() and self.current_token()[0] != 'RPAREN':
            arguments = self._parse_function_arguments(spreadsheet)
        
        # Expect closing parenthesis
        token = self.current_token()
        if not token or token[0] != 'RPAREN':
            raise SyntaxErrorException(f"Expected ')' to close function {func_name}")
        self.advance()  # consume ')'
        
        # Set arguments on function
        func_operand.arguments = arguments
        return func_operand

    def _parse_function_arguments(self, spreadsheet: Spreadsheet) -> List[FunctionArgument]:
        """Parse function arguments separated by semicolons"""
        arguments = []
        
        while True:
            arg = self._parse_function_argument(spreadsheet)
            if arg:
                arguments.append(arg)
            
            # Check for semicolon (more arguments) or end
            token = self.current_token()
            if not token:
                break
            elif token[0] == 'SEMI':
                self.advance()  # consume ';'
                continue
            elif token[0] == 'RPAREN':
                break
            else:
                raise SyntaxErrorException(f"Expected ';' or ')' in function arguments, got {token[1]}")
        
        return arguments

    def _parse_function_argument(self, spreadsheet: Spreadsheet) -> Union[FunctionArgument, None]:
        """Parse a single function argument"""
        token = self.current_token()
        if not token:
            return None
            
        token_type, token_value = token
        
        if token_type == 'NUMBER':
            self.advance()
            # Convert to numeric value
            value = float(token_value) if '.' in token_value else int(token_value)
            return NumericArgument(value)
            
        elif token_type == 'CELL':
            self.advance()
            # Create cell and wrap in CellArgument
            return CellArgument.create_from_token(token_value, spreadsheet)
            
        elif token_type == 'RANGE':
            self.advance()
            # Parse range like "A1:B3"
            start_ref, end_ref = token_value.split(':')
            return CellRangeArgument(start_ref, end_ref, spreadsheet)
            
        elif token_type == 'FUNC':
            # Handle nested function - parse it as a FunctionOperand and wrap it
            nested_function = self._parse_function(token_value, spreadsheet)
            return FunctionArgumentWrapper(nested_function)
            
        else:
            raise SyntaxErrorException(f"Invalid function argument: {token_type} '{token_value}'")