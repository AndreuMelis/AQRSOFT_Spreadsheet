# spreadsheet/formula/formula_element.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class FormulaElement(ABC):
    """
    Clase base para todos los elementos de una fórmula en notación *postfix*
    (RPN).  Sus subclases típicas son:

        • Operand   — envuelve valores (Number, CellOperand, FunctionOperand…)
        • Operator  — +, -, *, /, ^, …

    Cada elemento expone `accept(visitor)` para que un `FormulaElementVisitor`
    pueda despacharlo mediante *double-dispatch*.
    """

    __slots__ = ()  # Evita diccionario interno; ahorra memoria

    @abstractmethod
    def accept(self, visitor: "FormulaElementVisitor") -> Any:  # noqa: F821
        """
        Punto de entrada al patrón Visitor.

        Args:
            visitor (FormulaElementVisitor): Implementación concreta que sabrá
                cómo procesar el elemento (evaluación, serialización, etc.).

        Returns:
            Any: Valor devuelto por el visitor.  Normalmente será un número
                (`float`) en el caso del `PostfixEvaluationVisitor`, pero se
                deja abierto para otros usos (pretty-print, optimización…).
        """
        raise NotImplementedError
