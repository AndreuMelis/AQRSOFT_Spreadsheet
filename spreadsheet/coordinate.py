class Coordinate:
    def __init__(self, column: str, row: int):
        self._row = row
        self._column = column

    @property
    def column(self) -> str:
        return self._column

    @column.setter
    def column(self, value: str) -> None:
        self._column = value

    @property
    def row(self) -> int:
        return self._row

    @row.setter
    def row(self, value: int) -> None:
        self._row = value

    def __eq__(self, other):
        if not isinstance(other, Coordinate):
            return False
        return self._column == other._column and self._row == other._row

    def __hash__(self):
        return hash((self._column, self._row))
