from ui.terminal_ui import TerminalUI
import os
import re

from content.numerical_content import NumericContent
from content.text_content import TextContent
from content.formula_content import FormulaContent
from fileio.load_file import LoadFile
from fileio.save_file import SaveFile
from spreadsheet.spreadsheet import Spreadsheet
from spreadsheet.cell import Cell
from spreadsheet.coordinate import Coordinate
from ui.terminal_ui import TerminalUI

from exceptions import (
    InvalidFileNameException,
    InvalidFilePathException,
    FileNotFoundException,
    InvalidCellReferenceException,
    CircularDependencyException,
    InvalidPostfixException,
    EvaluationErrorException,
    SyntaxErrorException
)

class SpreadsheetController:
    def __init__(self, spreadsheet: Spreadsheet):
        self.UI = TerminalUI()
        self.spreadsheet: Spreadsheet = spreadsheet
        self.loader = LoadFile()
        self.saver = SaveFile()

    def run_menu(self):
        command = self.UI.display_menu()
        self.run_command(command)

    def run_command(self, command: str):
        while True:

            if command.startswith("RF"):
                self.read_commands_from_file(command.split(maxsplit=1)[1])
            elif command == "C":
                self.create_new_spreadsheet()
            elif command.startswith("E"):
                parts = command.split(maxsplit=2)
                if len(parts) == 3:
                    self.edit_cell(parts[1].upper(), parts[2])
                else:
                    print("Invalid command format. Use E <cell coordinate> <new cell content>")
            elif command.startswith("L"):
                self.load_spreadsheet(command.split(maxsplit=1)[1])
            elif command.startswith("S"):
                self.save_spreadsheet(self.spreadsheet)
            elif command == "X":
                print("Exiting program.")
                break
            else:
                print("Invalid command. Please try again.")

    def load_spreadsheet(self, file_path: str):
        try:
            self.loader.validate_file_format(file_path)
            raw_data = self.loader.load_spreadsheet_data(file_path)

            new_sheet = Spreadsheet()
            def num_to_col(num: int) -> str:
                col = ''
                while num > 0:
                    num, rem = divmod(num - 1, 26)
                    col = chr(rem + ord('A')) + col
                return col

            for row_idx, row_values in enumerate(raw_data, start=1):
                for col_idx, cell_text in enumerate(row_values):
                    text = cell_text.strip().rstrip(';')
                    if not text:
                        continue
                    col_letter = num_to_col(col_idx + 1)
                    coord = Coordinate(col_letter, row_idx)
                    if text.startswith('='):
                        content_obj = FormulaContent(text)
                    elif re.fullmatch(r"\d+\.\d+", text):
                        content_obj = NumericContent(float(text))
                    elif re.fullmatch(r"\d+", text):
                        content_obj = NumericContent(int(text))
                    else:
                        content_obj = TextContent(text)
                    new_sheet.add_cell(coord, Cell((col_letter, row_idx), content_obj))

            self.spreadsheet = new_sheet
            self.spreadsheet.print_spreadsheet()
            print("Spreadsheet loaded.")
        except (InvalidFilePathException, InvalidFileNameException, FileNotFoundException) as e:
            print(f"Error: {e}")

    def save_spreadsheet(self, spreadsheet: Spreadsheet):
        try:
            self.saver.run_saver(spreadsheet)
        except (InvalidFileNameException, InvalidFilePathException, FileNotFoundException) as e:
            print(f"Error: {e}")

    def create_new_spreadsheet(self):
        self.spreadsheet = Spreadsheet()
        self.spreadsheet.print_spreadsheet()
        print("New spreadsheet created.")

    def edit_cell(self, cell_coord: str, cell_content: str):
        try:
            column, row_num = self.parse_coordinate(cell_coord)
            coord = Coordinate(column, row_num)

            # Build the new content object
            if cell_content.startswith('='):
                content_obj = FormulaContent(cell_content)
            elif re.fullmatch(r"\d+\.\d+", cell_content):
                content_obj = NumericContent(float(cell_content))
            elif re.fullmatch(r"\d+", cell_content):
                content_obj = NumericContent(int(cell_content))
            else:
                content_obj = TextContent(cell_content)

            # Backup the previous cell (if any)
            prev_cell = self.spreadsheet.cells.get(coord)

            # Create new cell
            new_cell = Cell((column, row_num), content_obj)
            
            # Temporarily add the new cell to test for errors
            self.spreadsheet.add_cell(coord, new_cell)

            # Try to evaluate the cell content to check for errors
            try:
                if isinstance(content_obj, FormulaContent):
                    # Test evaluation by getting the cell value
                    # This will trigger any evaluation errors
                    new_cell.content.get_value(self.spreadsheet)
                
                # If we get here, no errors occurred - print the updated spreadsheet
                self.spreadsheet.print_spreadsheet()
                
            except (
                CircularDependencyException,
                InvalidPostfixException,
                EvaluationErrorException,
                SyntaxErrorException,
                RecursionError
            ) as e:
                # Roll back the cell change
                if prev_cell is not None:
                    self.spreadsheet.cells[coord] = prev_cell
                else:
                    self.spreadsheet.cells.pop(coord, None)

                # Print the error message
                print(f"Error: {e}")
                
                # Print the spreadsheet in its previous state
                self.spreadsheet.print_spreadsheet()

        except InvalidCellReferenceException as e:
            print(f"Error: {e}")


    def read_commands_from_file(self, file_path: str):
        try:
            with open(file_path, 'r') as cmd_file:
                for cmd_line in cmd_file:
                    cmd = cmd_line.strip()
                    self.execute_command(cmd[:2].upper() + cmd[2:])
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")

    def execute_command(self, cmd: str):
        if cmd.startswith("C"):
            self.create_new_spreadsheet()
        elif cmd.startswith("E"):
            parts = cmd.split(maxsplit=2)
            if len(parts) == 3:
                self.edit_cell(parts[1].upper(), parts[2])
            else:
                print("Invalid command format. Use E <cell coordinate> <new cell content>")
        elif cmd.startswith("L"):
            self.load_spreadsheet(cmd.split(maxsplit=1)[1])
        elif cmd.startswith("S"):
            self.save_spreadsheet(self.spreadsheet)
        else:
            print("Invalid command in file. Skipping.")

    def parse_coordinate(self, coord: str) -> tuple[str, int]:
        match = re.match(r"^([A-Z]+)(\d+)$", coord)
        if match:
            return match.group(1), int(match.group(2))
        raise InvalidCellReferenceException(f"Invalid cell coordinate: {coord}")

    def format_coordinate_for_display(self, coord: tuple[str, int]) -> str:
        column, row = coord
        return f"\033[34m{column}\033[0m\033[32m{row}\033[0m"
