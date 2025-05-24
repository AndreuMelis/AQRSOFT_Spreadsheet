import re
from exceptions.exception import SyntaxErrorException

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0
        self.function_stack = []  # Track nested functions

    def next_token(self):
        if self.current_index < len(self.tokens):
            token = self.tokens[self.current_index]
            self.current_index += 1
            return token
        return None

    def peek_token(self):
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        return None

    def parse(self):
        if not self.tokens:
            raise SyntaxErrorException("No tokens to parse")

        last_token_type = None
        parens_balance = 0
        expecting_range = False

        while self.current_index < len(self.tokens):
            token_type, token_value = self.next_token()

            if token_type == 'FUNC':
                if last_token_type in ['operand', 'RPAREN']:
                    raise SyntaxErrorException("Function cannot follow operand or closing bracket")
                self.function_stack.append(token_value)
                last_token_type = 'function'

            elif token_type == 'CELL':
                if last_token_type == 'operand' and not expecting_range:
                    raise SyntaxErrorException("Two consecutive operands")
                last_token_type = 'operand'
                expecting_range = True

            elif token_type == 'SEMI':
                if not self.function_stack or last_token_type in ['operator', 'LPAREN', 'SEMI']:
                    raise SyntaxErrorException("Misplaced ';' in arguments")
                last_token_type = 'SEMI'

            elif token_type == 'NUMBER':
                if last_token_type in ['operand', 'RPAREN']:
                    raise SyntaxErrorException("Number after operand without operator")
                last_token_type = 'operand'
                expecting_range = False

            elif token_type == 'COLON':
                if not expecting_range or last_token_type != 'operand':
                    raise SyntaxErrorException("Misplaced ':' in formula")
                last_token_type = 'range'
                expecting_range = False

            elif token_type in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE']:
                if last_token_type not in ['operand', 'RPAREN']:
                    raise SyntaxErrorException("Operator cannot be placed here")
                last_token_type = 'operator'

            elif token_type == 'LPAREN':
                parens_balance += 1
                if last_token_type in ['operand', 'RPAREN']:
                    raise SyntaxErrorException("Unexpected '(' after operand")
                last_token_type = 'LPAREN'

            elif token_type == 'RPAREN':
                parens_balance -= 1
                if parens_balance < 0:
                    raise SyntaxErrorException("Unmatched closing parenthesis")
                if last_token_type in ['operator', 'LPAREN']:
                    raise SyntaxErrorException("Unexpected ')' after operator or '('")
                last_token_type = 'RPAREN'
                if self.function_stack:
                    self.function_stack.pop()

            elif token_type == 'RANGE':
                if last_token_type == 'operand':
                    raise SyntaxErrorException("Unexpected range after operand")
                last_token_type = 'operand'

            else:
                raise SyntaxErrorException(f"Unknown token type: {token_type}")

        if parens_balance != 0:
            raise SyntaxErrorException("Unbalanced parentheses in formula")

        return True

    def is_coordinate(self, token):
        return re.match(r'^[A-Z]+\d+$', token) is not None

    def is_function(self, token):
        return token in ["SUMA", "PROMEDIO", "MAX", "MIN"]

    def is_number(self, token):
        return re.match(r'^\d+\.?\d*$', token) is not None
