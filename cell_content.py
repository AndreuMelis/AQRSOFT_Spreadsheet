from abc import ABC, abstractmethod

class CellContent(ABC):
    @abstractmethod
    def get_value(self):
        pass

class TextContent(CellContent):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def get_value(self):
        return self.text

class NumericContent(CellContent):
    def __init__(self, number: float):
        super().__init__()
        self.number = number

    def get_value(self):
        return self.number
        