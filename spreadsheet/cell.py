from content.cell_content import CellContent
from typing import Union, List, Any
from spreadsheet import Coordinate


class Cell:
    def __init__(self, coordinate: tuple, content: CellContent = None):
        self._coordinate = Coordinate(coordinate[0], coordinate[1])
        self._content = content

    # TODO -> check how return of coordinates is needed
    @property
    def coordinate(self) -> tuple:
        return self._coordinate
    
    @coordinate.setter
    def coordinate(self, coordinate: tuple) -> None:
        self._coordinate = Coordinate(coordinate[0], coordinate[1])

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


