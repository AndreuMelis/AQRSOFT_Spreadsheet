# --------------------------------------------------------------------------------------------------
# Archivo: usecasesmarker/spreadsheet_controller_for_checker.py
# --------------------------------------------------------------------------------------------------
import os
import re

from content.numerical_content import NumericContent
from content.text_content import TextContent
from content.formula_content import FormulaContent
from spreadsheet.coordinate import Coordinate
from fileio.load_file import LoadFile
from fileio.save_file import SaveFile

from spreadsheet.spreadsheet import Spreadsheet
from spreadsheet.cell import Cell
from spreadsheet.coordinate import Coordinate  # ADD THIS IMPORT

import exceptions as ex
from usecasesmarker.reading_spreadsheet_exception import ReadingSpreadsheetException
from usecasesmarker.saving_spreadsheet_exception import SavingSpreadsheetException


class ISpreadsheetControllerForChecker:
    """
    Interface class for spreadsheet controller with methods for setting and retrieving
    cell content, and for loading/saving from disk using the existing fileio helpers.
    """

    def __init__(self):
        # Initialize an empty spreadsheet
        self.spreadsheet = Spreadsheet()
        # Helpers for load/save
        self._loader = LoadFile()
        self._saver  = SaveFile()

    def set_cell_content(self, coord: str, str_content: str):
        """
        Sets the content of a spreadsheet cell.
        Supports formulas (starting with '='), numeric, and text content.
        Raises BadCoordinateException or CircularDependencyException as needed.
        """
        content = str(str_content)
        m = re.fullmatch(r"([A-Z]+)(\d+)", coord)
        if not m:
            raise ex.BadCoordinateException(f"Invalid Cell: {coord}")
        col, row = m.group(1), int(m.group(2))

        if content.startswith('='):
            # Keep the leading '=' so FormulaContent.validate_formula_format() passes
            cell_content = FormulaContent(content)
        elif re.fullmatch(r"\d+\.\d+", content):
            cell_content = NumericContent(float(content))
        elif re.fullmatch(r"\d+", content):
            cell_content = NumericContent(int(content))
        else:
            cell_content = TextContent(content)

        # FIX: Create Coordinate object instead of passing tuple
        coordinate = Coordinate(col, row)
        self.spreadsheet.add_cell(coordinate, Cell((col, row), cell_content))

    def get_cell_content_as_float(self, coord: str) -> float:
        """
        Retrieves the numeric value of a cell, converting it to float.
        Raises BadCoordinateException or NoNumberException if conversion fails.
        """
        m = re.fullmatch(r"([A-Z]+)(\d+)", coord)
        if not m:
            raise ex.BadCoordinateException(f"Invalid cell: {coord}")
        col, row = m.group(1), int(m.group(2))

        # FIX: Create Coordinate object instead of passing tuple
        coordinate = Coordinate(col, row)
        cell = self.spreadsheet.get_cell(coordinate)
        if not cell:
            raise ex.BadCoordinateException(f"Cell not found: {coord}")

        val = cell.get_value(self.spreadsheet)
        try:
            return float(val)
        except (ValueError, TypeError):
            raise ex.NoNumberException(f"Cell content is not a valid float: {val}")

    def get_cell_content_as_string(self, coord: str) -> str:
        """
        Retrieves the content of a cell as a string.
        Raises BadCoordinateException if the cell does not exist.
        """
        m = re.fullmatch(r"([A-Z]+)(\d+)", coord)
        if not m:
            raise ex.BadCoordinateException(f"Invalid cell: {coord}")
        col, row = m.group(1), int(m.group(2))

        # FIX: Create Coordinate object instead of passing tuple
        coordinate = Coordinate(col, row)
        cell = self.spreadsheet.get_cell(coordinate)
        if not cell:
            raise ex.BadCoordinateException(f"Cell not found: {coord}")

        return str(cell.get_value(self.spreadsheet))

    def get_cell_formula_expression(self, coord: str) -> str:
        """
        Retrieves the raw formula (with leading '=') from a cell.
        Raises BadCoordinateException if there's no formula.
        """
        m = re.fullmatch(r"([A-Z]+)(\d+)", coord)
        if not m:
            raise ex.BadCoordinateException(f"Invalid cell: {coord}")
        col, row = m.group(1), int(m.group(2))

        # FIX: Create Coordinate object instead of passing tuple
        coordinate = Coordinate(col, row)
        cell = self.spreadsheet.get_cell(coordinate)
        if not cell or not isinstance(cell.content, FormulaContent):
            raise ex.BadCoordinateException(f"No formula in cell: {coord}")

        return "=" + cell.content.formula

    def save_spreadsheet_to_file(self, s_name_in_user_dir: str):
        """
        Saves the current spreadsheet to a .s2v file in the working directory.
        Raises SavingSpreadsheetException on error.
        """
        # Ensure .s2v extension
        file_name = s_name_in_user_dir
        if not file_name.lower().endswith(".s2v"):
            file_name += ".s2v"
        directory = os.getcwd()

        try:
            self._saver.validate_file_name(file_name)
            self._saver.validate_directory(directory)

            # Columns from A to Z
            # Get only the column letters present in the spreadsheet
            letters = sorted({coord.column for coord in self.spreadsheet.cells.keys()})
            max_row = max((coord.row for coord in self.spreadsheet.cells.keys()), default=0)

            # Build a 2D list of strings (each row is a list of cell values)
            spreadsheet_data = []
            for row in range(1, max_row + 1):
                row_list = []
                for col in letters:
                    coord = Coordinate(col, row)
                    cell = self.spreadsheet.cells.get(coord)
                    if cell and cell.content is not None:
                        value = cell.get_textual_representation()
                        cell_str = str(value).replace(";", ",")
                    else:
                        cell_str = ''
                    row_list.append(cell_str)
                spreadsheet_data.append(row_list)

            # Actually write to file, joining each row with semicolons
            self._saver.save_spreadsheet_data(file_name, directory, spreadsheet_data)

        except Exception as e:
            raise SavingSpreadsheetException(
                f"Failed to save spreadsheet to {file_name}: {e}"
            ) from e

    def load_spreadsheet_from_file(self, s_name_in_user_dir: str):
        """
        Loads a spreadsheet from a .s2v file (semicolon-delimited) on disk.
        Raises ReadingSpreadsheetException on error.
        """
        path = os.path.abspath(s_name_in_user_dir)
        try:
            # Validate & read raw CSV data
            self._loader.validate_file_format(path)
            raw = self._loader.load_spreadsheet_data(path)

            # Build a fresh Spreadsheet
            new_sheet = Spreadsheet()
            def num_to_col(n: int) -> str:
                col = ''
                while n > 0:
                    n, rem = divmod(n - 1, 26)
                    col = chr(rem + ord('A')) + col
                return col

            for row_idx, row_values in enumerate(raw, start=1):
                for col_idx, cell_text in enumerate(row_values):
                    text = cell_text.strip().rstrip(';')
                    if not text:
                        continue
                    col_letter = num_to_col(col_idx + 1)
                    # FIX: Create Coordinate object instead of passing tuple
                    coordinate = Coordinate(col_letter, row_idx)

                    if text.startswith('='):
                        content = FormulaContent(text)
                    elif re.fullmatch(r"\d+\.\d+", text):
                        content = NumericContent(float(text))
                    elif re.fullmatch(r"\d+", text):
                        content = NumericContent(int(text))
                    else:
                        content = TextContent(text)

                    new_sheet.add_cell(coordinate, Cell((col_letter, row_idx), content))

            self.spreadsheet = new_sheet

        except Exception as e:
            raise ReadingSpreadsheetException(
                f"Failed to load spreadsheet from {path}: {e}"
            ) from e