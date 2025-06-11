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
    from content.formula_content import FormulaContent
    from content.numerical_content import NumericContent
    from content.text_content import TextContent


class Cell:
    def __init__(self, coordinate: tuple[str, int], content: CellContent | None = None):
        # coordinate viene como ("A", 1), por ejemplo
        self._coordinate = Coordinate(coordinate[0], coordinate[1])
        self._content: FormulaContent | NumericContent | TextContent | None = content

    @property
    def coordinate(self) -> Coordinate:
        return self._coordinate
    
    @coordinate.setter
    def coordinate(self, coordinate):
        """Set the coordinate of the cell."""
        # FIXED: Handle both Coordinate objects and tuples
        if isinstance(coordinate, Coordinate):
            self._coordinate = coordinate
        else:
            # Handle tuple case (col, row)
            self._coordinate = Coordinate(coordinate[0], coordinate[1])

    @property
    def content(self) -> CellContent | None:
        return self._content
    
    @content.setter # not used, subsituted by get_value
    def content(self, content: CellContent) -> None:
        self._content = content

    def get_textual_representation(self) -> str:
        """
        Devuelve la representación textual del contenido de la celda.
        """
        return self._content.get_text() if self.content else ""
    
    def get_value(self, spreadsheet: Optional["Spreadsheet"] = None):
        """
        Devuelve el valor calculado por el content.
        Si el contenido es fórmula, puede necesitar 'spreadsheet' para resolver referencias.
        """
        # Import here to avoid circular imports
        from content.formula_content import FormulaContent
        
        if isinstance(self._content, FormulaContent) and spreadsheet is not None:
            # For formulas, pass the current cell name to avoid circular dependency issues
            current_cell_name = f"{self._coordinate.column}{self._coordinate.row}"
            return self._content.get_value(spreadsheet, current_cell_name)
        else:
            return self._content.get_value()

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