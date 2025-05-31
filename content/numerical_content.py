from typing import Union

from content.cell_content import CellContent
from content.number import Number, NumberValue


class NumericContent(CellContent):
    def __init__(self, number: Union[Number, NumberValue]):
        # Acepta tanto Number como valor crudo
        self.number = number if isinstance(number, Number) else Number(number)

    # API pública
    def get_number(self) -> float:
        return self.number.get_value()

    def get_text(self) -> str:
        return str(self.number)

    def get_value(self, spreadsheet):  # spreadsheet no se usa, pero mantiene la firma
        return self.get_number()

    # Setter opcional
    def set_number(self, value: NumberValue) -> None:
        self.number.value = value
