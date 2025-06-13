from abc import ABC, abstractmethod
import re
from typing import Union, Any, List, Dict, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from .formula_element import FormulaElementVisitor
    from .function import Function, FunctionArgument
    from spreadsheet.spreadsheet import Spreadsheet

from content.numerical_content import NumericContent
from spreadsheet.cell import Cell
from spreadsheet.coordinate import Coordinate
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
    def create_from_token(cls, token_value, spreadsheet: 'Spreadsheet' = None) -> "Operand":
        pass

class NumericOperand(Operand):
    """Representa un literal numérico."""

    def __init__(self, value: Union[int, float]) -> None:
        self.value: Number = Number(value)

    def get_value(self) -> Union[int, float]:
        return self.value.get_value()

    @classmethod
    def create_from_token(cls, token_value) -> "NumericOperand":
        if '.' in str(token_value):
            return cls(float(token_value))
        else:
            return cls(int(token_value))


class CellOperand(Operand):
    """Represents a reference to a cell in the spreadsheet.
    Missing cells are treated as zero, and never embed errors in the sheet."""

    def __init__(self, cell: 'Cell') -> None:
        self.cell = cell

    def get_value(self) -> Union[int, float]:
        return self.cell.content.get_value()

    @classmethod
    def create_from_token(cls, token_value, spreadsheet: "Spreadsheet" = None) -> "CellOperand":
        if spreadsheet is None:
            raise ValueError("Spreadsheet is required to create CellOperand")

        tok = str(token_value).upper()
        m = re.fullmatch(r"([A-Z]+)(\d+)", tok)
        if not m:
            raise ValueError(f"Invalid cell reference: {token_value}")
        col, row = m.groups()

        cell = spreadsheet.get_cell(Coordinate(col, int(row)))
        if cell is None:
            coord_tuple = (col, row)
            placeholder = Cell(coord_tuple, NumericContent(0.0))
            spreadsheet.add_cell(Coordinate(col, int(row)), placeholder)
            cell = placeholder
        else:
            setattr(cell, "_sheet", spreadsheet)

        return cls(cell)
class FunctionOperand(Operand):
    """Representa una función (SUMA, PROMEDIO, MAX, MIN, etc.) sin argumentos inicializados."""

    def __init__(self, func: "Function", arguments: List["FunctionArgument"] = None) -> None:
        self.function: "Function" = func
        self.arguments: List["FunctionArgument"] = arguments or []

    def get_value(self) -> Union[int, float]:
        values: List[Union[int, float]] = []
        for arg in self.arguments:
            v = arg.get_value()
            if isinstance(v, list):
                values.extend(v)
            else:
                values.append(v)
        return self.function.evaluate(values)

    @classmethod
    def create_from_token(cls, token_value, spreadsheet: 'Spreadsheet' = None) -> "FunctionOperand":
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
