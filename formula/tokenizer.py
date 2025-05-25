import re
from exceptions import TokenizingErrorException  # Adjust the import path if needed

class Tokenizer:
    def __init__(self):
        # Define all token patterns with clear naming
        self.token_specification = [
            ('RANGE', r'[A-Z]+\d+:[A-Z]+\d+'),             # Cell ranges like A1:B3
            ('FUNC', r'SUMA|PROMEDIO|MAX|MIN'),            # Functions
            ('CELL', r'[A-Z]+\d+'),                        # Single cell references
            ('NUMBER', r'\d+(\.\d+)?'),                    # Numbers (integer or decimal)
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('TIMES', r'\*'),
            ('DIVIDE', r'/'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('SEMI', r';'),
            ('COLON', r':'),
            ('SKIP', r'[ \t]+'),                           # Skip whitespace
            ('MISMATCH', r'.'),                            # Catch-all for unexpected characters
        ]
        self.token_regex = re.compile('|'.join(
            f'(?P<{name}>{pattern})' for name, pattern in self.token_specification
        ))

    def tokenize(self, formula):
        tokens = []
        pos = 0

        while pos < len(formula):
            match = self.token_regex.match(formula, pos)
            if not match:
                raise TokenizingErrorException(f"Unexpected character at position {pos}: '{formula[pos]}'")

            kind = match.lastgroup
            value = match.group(kind)

            if kind == 'SKIP':
                pass  # Ignore whitespace
            elif kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
                tokens.append((kind, value))
            elif kind == 'MISMATCH':
                raise TokenizingErrorException(f"Incorrect formula: '{value}' in '{formula}'")
            else:
                tokens.append((kind, value))

            pos = match.end()

        return tokens
