from cell import Cell

class Spreadsheet():
    def __init__(self):
        self.cells = {}

    def get_cell(self, coords: tuple) -> Cell:
        return self.cells.get(coords)
    
    def add_cell(self, coords: tuple, cell: Cell) -> None:
        self.cells[coords] = cell
    
    