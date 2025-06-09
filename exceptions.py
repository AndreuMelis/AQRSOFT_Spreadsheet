# all our custom exceptions

#  Use Case 1 Exceptions
class InvalidFileNameException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class InvalidFilePathException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class FileNotFoundException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)


#Use Case 3 Exceptions
class InvalidContentFormatException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class UnsupportedContentTypeException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)


# Use Case 5 Exceptions
class TokenizingErrorException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class SyntaxErrorException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class CircularDependencyException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class ConversionException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class EvaluationErrorException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class InvalidPostfixException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class InvalidCellReferenceException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class CellValueException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class FunctionEvaluationException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class InvalidArgumentException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class MathematicalEvaluationException(Exception):
    def __init__(self, mssg=None):
        super().__init__(mssg)

class BadCoordinateException(Exception):
    """Raised when a cell coordinate is syntactically invalid or refers to no cell."""
    def __init__(self, mssg=None):
        super().__init__(mssg)

class NoNumberException(Exception):
    """Raised when a cell’s content cannot be converted to a number."""
    def __init__(self, mssg=None):
        super().__init__(mssg)
