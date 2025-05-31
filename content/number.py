from __future__ import annotations  # Para anotaciones del propio módulo
from typing import Union

NumberValue = Union[int, float]


class Number:
    """Value Object simple que envuelve un número y aplica validación."""

    __slots__ = ("_value",)

    def __init__(self, value: NumberValue):
        self.value = value  # Setter valida

    # Propiedad
    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, v: NumberValue):
        if not isinstance(v, (int, float)):
            raise TypeError("Number must be int or float")
        self._value = float(v)

    # API unificada
    def get_value(self) -> float:
        return self._value

    # Conversión cómoda
    def __float__(self) -> float:
        return self._value

    def __str__(self) -> str:
        return str(self._value)