# --------------------------------------------------------------------------------------------------
# Archivo: spreadsheet/cell.py
# --------------------------------------------------------------------------------------------------
from content.cell_content import CellContent
from .coordinate import Coordinate
import re
from typing import Optional, Any, TYPE_CHECKING

# Si se desea usar "Spreadsheet" como type hint sin que se importe en tiempo de ejecución:
if TYPE_CHECKING:
    from .spreadsheet import Spreadsheet


class Cell:
    def __init__(self, coordinate: tuple[str, int], content: CellContent | None = None):
        # coordinate viene como ("A", 1), por ejemplo
        self._coordinate = Coordinate(coordinate[0], coordinate[1])
        self._content = content

    @property
    def coordinate(self) -> Coordinate:
        return self._coordinate
    
    @coordinate.setter
    def coordinate(self, coordinate: tuple[str, int]) -> None:
        self._coordinate = Coordinate(coordinate[0], coordinate[1])

    @property
    def content(self) -> CellContent | None:
        return self._content
    
    @content.setter
    def content(self, content: CellContent) -> None:
        self._content = content

    def get_value(self, spreadsheet: Optional["Spreadsheet"] = None):
        """
        Devuelve el valor calculado por el content.
        Si el contenido es fórmula, puede necesitar 'spreadsheet' para resolver referencias.
        """
        return self.content.get_value(spreadsheet)

    @staticmethod
    def from_token(token_value: str, spreadsheet: "Spreadsheet" = None) -> "Cell":
        """
        Crea una instancia de Cell buscando en el spreadsheet la celda ya existente.
        token_value = "A1", "B2", etc.
        IMPORTAMOS Spreadsheet solo dentro de este método para evitar ciclos.
        """
        if spreadsheet is None:
            raise ValueError("Spreadsheet is required to create Cell from token")

        match = re.match(r'^([A-Z]+)(\d+)$', str(token_value))
        if not match:
            raise ValueError(f"Invalid cell reference: {token_value}")
        
        col_str, row_str = match.groups()
        coords = Coordinate(col_str, int(row_str))
        return spreadsheet.get_cell(coords)
