# --------------------------------------------------------------------------------------------------
# Archivo: formula/operand.py
# --------------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import Union, Any, List, Dict, Type, TYPE_CHECKING

# Importamos solo para type‐checking, no en ejecución
if TYPE_CHECKING:
    from .formula_element import FormulaElementVisitor, FormulaElement
    from .operator import Operator
    from .function import Function, FunctionArgument

# Importamos el resto de dependencias externas
from spreadsheet.cell import Cell
from spreadsheet.coordinate import Coordinate
from spreadsheet.spreadsheet import Spreadsheet

from content.number import Number

class Operand(ABC):
    """Clase base para operandos (números, referencias a celdas, funciones)."""

    @abstractmethod
    def get_value(self) -> Union[int, float]:
        pass

    def accept(self, visitor: "FormulaElementVisitor") -> Any:
        return visitor.visit_operand(self)

    @classmethod
    @abstractmethod
    def create_from_token(cls, token_value, spreadsheet: Spreadsheet = None) -> "Operand":
        pass


class NumericOperand(Operand):
    """Representa un literal numérico."""

    def __init__(self, value: Union[int, float]) -> None:
        self.value: Number = Number(value)

    def get_value(self) -> Union[int, float]:
        return self.value.get_value()

    @classmethod
    def create_from_token(cls, token_value, spreadsheet: Spreadsheet = None) -> "NumericOperand":
        if '.' in str(token_value):
            return cls(float(token_value))
        else:
            return cls(int(token_value))


class CellOperand(Operand):
    """Representa la referencia a una celda en el spreadsheet."""

    def __init__(self, cell: Cell) -> None:
        self.cell = cell

    def get_value(self) -> Union[int, float, str]:
        return self.cell.get_value()

    @classmethod
    def create_from_token(cls, token_value, spreadsheet: Spreadsheet = None) -> "CellOperand":
        if spreadsheet is None:
            raise ValueError("Spreadsheet is required to create CellOperand")
        cell = Cell.from_token(token_value, spreadsheet)
        return cls(cell)


class FunctionOperand(Operand):
    """Representa una función (SUMA, PROMEDIO, MAX, MIN, etc.) sin argumentos inicializados."""

    def __init__(self, func: "Function", arguments: List["FunctionArgument"] = None) -> None:
        self.function: "Function" = func
        self.arguments: List["FunctionArgument"] = arguments or []

    def get_value(self, spreadsheet: Spreadsheet = None) -> Union[int, float]:
        values: List[Union[int, float]] = []
        for arg in self.arguments:
            v = arg.get_value(spreadsheet)
            if isinstance(v, list):
                values.extend(v)
            else:
                values.append(v)
        return self.function.evaluate(values)

    @classmethod
    def create_from_token(cls, token_value, spreadsheet: Spreadsheet = None) -> "FunctionOperand":
        function_name = str(token_value).upper()

        from .function import SUMA, PROMEDIO, MAX, MIN
        function_map: Dict[str, Type["Function"]] = {
            "SUMA": SUMA,
            "SUM": SUMA,
            "PROMEDIO": PROMEDIO,
            "AVERAGE": PROMEDIO,
            "MAX": MAX,
            "MIN": MIN,
        }

        if function_name in function_map:
            func = function_map[function_name]()  # instancia la clase de función
            return cls(func)
        else:
            raise ValueError(f"Unknown function: {function_name}")
