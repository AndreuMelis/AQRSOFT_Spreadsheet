from cell_content import CellContent

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
