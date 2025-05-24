from content.cell_content import CellContent
from typing import Union, List, Any
class Cell:
    def __init__(self, coordinate: tuple, content: CellContent = None):
        self._coordinate = coordinate
        self._content = content

    @property
    def coordinate(self) -> tuple:
        return self._coordinate
    
    @coordinate.setter
    def coordinate(self, value: tuple) -> None:
        self._coordinate = value

    @property
    def content(self) -> CellContent:
        return self._content
    
    @content.setter
    def content(self, content: CellContent) -> None:
        self._content = content

    # Thanks to abstract class CellContent
    def get_value(self):
        return self.content.get_value()
    
    # def store_content_in_cell(self):

class Number:
    def __init__(self, value: Union[int, float]):
        self._value = value
    
    @property
    def value(self) -> Union[int, float]:
        return self._value

    @value.setter
    def value(self, value: Union[int, float]):
        self._value = value
    
    def get_value(self):
        return self._value


class CellRange:
        def __init__(self, origin: str, destination: str) -> None:
            self.origin_cell = origin
            self.dest_cell = destination
        # TODO
        def get_cells(self, spreadsheet) -> List[Cell]:
            """
            Use spreadsheet to resolve cell references (e.g. "A1" to Cell object)
            and return a flat list of Cell objects between origin and destination.
            """
            # Implement logic to return all cells in the range as Cell objects
            pass

        def get_values(self, spreadsheet) -> List[Any]:
            return [cell.get_value() for cell in self.get_cells(spreadsheet)]