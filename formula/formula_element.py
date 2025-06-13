from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .operand import Operand
    from .operator import Operator
    from .function import Function

class FormulaElementVisitor(ABC):
    """Visitor interface para elementos de fórmula (operandos, operadores, funciones)."""

    @abstractmethod
    def visit_operand(self, operand: "Operand") -> None:
        pass

    @abstractmethod
    def visit_operator(self, operator: "Operator") -> None:
        pass

class FormulaElement(ABC):
    """Clase base para todos los elementos de una expresión postfix (operandos, operadores, funciones)."""
    
    @abstractmethod
    def accept(self, visitor: FormulaElementVisitor) -> Any:
        pass

