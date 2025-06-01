# ui/TerminalUI.py
import os
import re

from content.numerical_content import NumericContent
from content.text_content      import TextContent
from content.formula_content   import FormulaContent
from fileio.load_file              import LoadFile
from fileio.save_file              import SaveFile
from spreadsheet.spreadsheet   import Spreadsheet
from spreadsheet.cell          import Cell
from exceptions                import (
    InvalidFileNameException,
    InvalidFilePathException,
    FileNotFoundException,
    InvalidCellReferenceException
)

class TerminalUI:
    def __init__(self, spreadsheet: Spreadsheet):
        self.sheet = spreadsheet
        self.loader = LoadFile()
        self.saver = SaveFile()

    def display_menu(self):
        print("\033[33m\n--- Spreadsheet Menu ---\033[0m")
        print("\033[36mRF <text file pathname> - Read commands from File\033[0m")
        print("\033[36mC - Create a New Spreadsheet\033[0m")
        print("\033[36mE <cell coordinate> <new cell content> - Edit a cell\033[0m")
        print("\033[36mL <SV2 file pathname> - Load a Spreadsheet from a file\033[0m")
        print("\033[36mS <SV2 file pathname> - Save the Spreadsheet to a file\033[0m")
        print("\033[31mX - Exit\033[0m")

    def run(self):
        while True:
            self.display_menu()
            user_input = input("Enter command: ").strip()
            command = user_input[:2].upper() + user_input[2:]

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
                self.save_spreadsheet(self.sheet)
            elif command == "X":
                print("Exiting program.")
                break
            else:
                print("Invalid command. Please try again.")

    def read_commands_from_file(self, file_path):
        try:
            with open(file_path, 'r') as cmd_file:
                for cmd_line in cmd_file:
                    cmd = cmd_line.strip()
                    self.execute_command(cmd[:2].upper() + cmd[2:])
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")

    def execute_command(self, cmd):
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
            self.save_spreadsheet(self.sheet)
        else:
            print("Invalid command in file. Skipping.")

    def create_new_spreadsheet(self):
        self.sheet = Spreadsheet()
        self.sheet.print_spreadsheet()
        print("New spreadsheet created.")

    def edit_cell(self, cell_coord: str, cell_content: str):
        try:
            column, row_num = self.parse_coordinate(cell_coord.upper())

            # Elegimos el tipo de contenido según el texto ingresado
            if cell_content.startswith('='):
                content_obj = FormulaContent(cell_content)
            elif cell_content.isdigit():
                content_obj = NumericContent(float(cell_content))
            else:
                content_obj = TextContent(cell_content)

            new_cell = Cell((column, row_num), content_obj)
            self.sheet.add_cell((column, row_num), new_cell)
            self.sheet.print_spreadsheet()
        except InvalidCellReferenceException as err:
            print(f"Error: {err}")

    def load_spreadsheet(self, file_path: str):
        try:
            self.loader.validate_file_format(file_path)
            spreadsheet_data = self.loader.load_spreadsheet_data(file_path)
            self.loader.show.printContentSpreadsheet(spreadsheet_data)
            print("Spreadsheet loaded.")
        except (InvalidFilePathException, InvalidFileNameException, FileNotFoundException) as e:
            print(f"Error: {e}")

    def save_spreadsheet(self, spreadsheet: Spreadsheet):
        try:
            self.saver.run_saver(spreadsheet)
        except (InvalidFileNameException, InvalidFilePathException, FileNotFoundException) as e:
            print(f"Error: {e}")

    def parse_coordinate(self, coord: str) -> tuple[str, int]:
        import re
        match = re.match(r"^([A-Z]+)(\d+)$", coord)
        if match:
            column = match.group(1)
            row = int(match.group(2))
            return column, row
        else:
            raise InvalidCellReferenceException(f"Invalid cell coordinate: {coord}")

    def format_coordinate_for_display(self, coord: tuple[str, int]) -> str:
        column, row = coord
        return f"\033[34m{column}\033[0m\033[32m{row}\033[0m"
