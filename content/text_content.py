# spreadsheet/content/text_content.py
from content.cell_content import CellContent


class TextContent(CellContent):
    def __init__(self, text: str = ""):
        self.text = text

    # Conversión a número (opcional)
    def get_number(self) -> float:
        if self.text == "":
            raise ValueError("Empty text cannot be converted to number")
        try:
            return float(self.text)
        except ValueError as exc:
            raise ValueError(f"'{self.text}' is not a valid number") from exc

    # Obligatorio
    def get_text(self) -> str:
        return self.text

    def get_value(self):
        return self.text

    # Mutador
    def set_text(self, text: str) -> None:
        self.text = text
