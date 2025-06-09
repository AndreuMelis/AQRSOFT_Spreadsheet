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

# Import the entities exceptions that the test framework expects
from entities.circular_dependency_exception import CircularDependencyException
from entities.bad_coordinate_exception import BadCoordinateException
from entities.no_number_exception import NoNumberException


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
            raise BadCoordinateException(f"Invalid Cell: {coord}")
        col, row = m.group(1), int(m.group(2))

        if content.startswith('='):
            # Keep the leading '=' so FormulaContent.validate_formula_format() passes
            cell_content = FormulaContent(content)
            
            # For formulas, check circular dependencies BEFORE adding the cell
            # This must happen before the cell is added to prevent circular references
            raw_expression = content[1:].replace(',', ';')
            tokens = cell_content.tokenize(raw_expression)
            try:
                cell_content.check_circular_dependencies(self.spreadsheet, tokens, coord.upper())
            except ex.CircularDependencyException as e:
                # Re-raise using the entities exception that the test expects
                raise CircularDependencyException(str(e))
                    
        elif re.fullmatch(r"\d+(?:\.\d+)?", content):
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
            raise BadCoordinateException(f"Invalid cell: {coord}")
        col, row = m.group(1), int(m.group(2))

        # FIX: Create Coordinate object instead of passing tuple
        coordinate = Coordinate(col, row)
        cell = self.spreadsheet.get_cell(coordinate)
        if not cell:
            raise BadCoordinateException(f"Cell not found: {coord}")

        val = cell.get_value(self.spreadsheet)
        try:
            return float(val)
        except (ValueError, TypeError):
            raise NoNumberException(f"Cell content is not a valid float: {val}")

    def get_cell_content_as_string(self, coord: str) -> str:
        """
        Retrieves the content of a cell as a string.
        Returns empty string if the cell does not exist (instead of throwing exception).
        """
        m = re.fullmatch(r"([A-Z]+)(\d+)", coord)
        if not m:
            raise BadCoordinateException(f"Invalid cell: {coord}")
        col, row = m.group(1), int(m.group(2))

        # FIX: Create Coordinate object instead of passing tuple
        coordinate = Coordinate(col, row)
        cell = self.spreadsheet.get_cell(coordinate)
        if not cell:
            # Return empty string instead of throwing exception for non-existent cells
            return ""

        # Use textual representation instead of calculated value
        return cell.get_textual_representation()

    def get_cell_formula_expression(self, coord: str) -> str:
        """
        Retrieves the raw formula (with leading '=') from a cell.
        Raises BadCoordinateException if there's no formula.
        """
        m = re.fullmatch(r"([A-Z]+)(\d+)", coord)
        if not m:
            raise BadCoordinateException(f"Invalid cell: {coord}")
        col, row = m.group(1), int(m.group(2))

        # FIX: Create Coordinate object instead of passing tuple
        coordinate = Coordinate(col, row)
        cell = self.spreadsheet.get_cell(coordinate)
        if not cell or not isinstance(cell.content, FormulaContent):
            raise BadCoordinateException(f"No formula in cell: {coord}")

        # Return the formula as stored (which should already include the '=')
        return cell.content.formula

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

            # Find the actual bounds of the spreadsheet
            if not self.spreadsheet.cells:
                # Empty spreadsheet
                data = []
            else:
                # Find max row
                max_row = max((coord.row for coord in self.spreadsheet.cells.keys()), default=0)
                
                data = []
                for r in range(1, max_row + 1):
                    # For each row, find the rightmost column that has data
                    row_cells = {}
                    max_col_num = 0
                    
                    for coord in self.spreadsheet.cells.keys():
                        if coord.row == r:
                            # Convert column letter to number (A=1, B=2, etc.)
                            col_num = 0
                            for char in coord.column:
                                col_num = col_num * 26 + (ord(char) - ord('A') + 1)
                            row_cells[col_num] = coord
                            max_col_num = max(max_col_num, col_num)
                    
                    # Build row values only up to the rightmost column with data
                    row_vals = []
                    for col_num in range(1, max_col_num + 1):
                        if col_num in row_cells:
                            coord = row_cells[col_num]
                            cell = self.spreadsheet.get_cell(coord)
                            if cell and cell.content is not None:
                                # Get the textual representation (formulas, not calculated values)
                                v = cell.get_textual_representation()
                                # For numeric content, avoid .0 suffix for integers
                                if cell.content.__class__.__name__ == 'NumericContent':
                                    try:
                                        num_val = float(v)
                                        if num_val.is_integer():
                                            v = str(int(num_val))
                                    except:
                                        pass
                            else:
                                v = ''
                        else:
                            v = ''
                        # replace any ';' to avoid breaking the format
                        row_vals.append(str(v).replace(";", ","))
                    
                    # Only add the row if it has at least one non-empty cell
                    if any(val for val in row_vals):
                        data.append(row_vals)
                    else:
                        data.append([])

            # Actually write to file, joining each row with semicolons
            self._saver.save_spreadsheet_data(file_name, directory, data)

        except Exception as e:
            raise SavingSpreadsheetException(
                f"Failed to save spreadsheet to {file_name}: {e}"
            ) from e

    def load_spreadsheet_from_file(self, s_name_in_user_dir: str):
        """
        Loads a spreadsheet from a .s2v file (semicolon-delimited) on disk.
        Raises ReadingSpreadsheetException on error.
        """
        import re  # Move import to the top of the method
        
        # First try the provided path as-is (relative to current directory)
        if not os.path.isabs(s_name_in_user_dir):
            path = os.path.join(os.getcwd(), s_name_in_user_dir)
        else:
            path = s_name_in_user_dir
            
        # If file doesn't exist, try looking in the markerrun directory
        if not os.path.exists(path):
            markerrun_path = os.path.join(os.getcwd(), "markerrun", s_name_in_user_dir)
            if os.path.exists(markerrun_path):
                path = markerrun_path
        
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
                        # Convert commas to semicolons in SUMA functions when loading
                        # but preserve commas between top-level arguments that are functions
                        if "SUMA(" in text:
                            def replace_suma_commas(match):
                                full_match = match.group(0)  # The entire SUMA(...) match
                                content = full_match[5:-1]   # Remove "SUMA(" and ")"
                                
                                # Parse arguments more carefully
                                result = ""
                                paren_depth = 0
                                for char in content:
                                    if char == '(':
                                        paren_depth += 1
                                        result += char
                                    elif char == ')':
                                        paren_depth -= 1
                                        result += char
                                    elif char == ',' and paren_depth == 0:
                                        # This is a top-level comma, check if it's before a function
                                        # Look ahead to see if the next argument starts with a function name
                                        remaining = content[len(result)+1:].strip()
                                        if remaining.startswith(('MIN(', 'MAX(', 'PROMEDIO(', 'SUMA(')):
                                            result += ','  # Keep comma before functions
                                        else:
                                            result += ';'  # Replace with semicolon for regular arguments
                                    else:
                                        result += char
                                
                                return f"SUMA({result})"
                            
                            pattern = r'SUMA\([^()]*(?:\([^()]*\)[^()]*)*\)'
                            text = re.sub(pattern, replace_suma_commas, text)
                        
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