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

class TerminalUI:
    def __init__(self):
        pass

    def display_menu(self):
        print("\033[1;4;36m\n====== SPREADSHEET MENU ======\033[0m")
        print("\033[1;33m[File]\033[0m")
        print("  \033[1;36mRF <text file pathname>\033[0m  - \033[3mRead commands from file\033[0m")
        print("  \033[1;36mL  <SV2 file pathname>\033[0m   - \033[3mLoad spreadsheet from file\033[0m")
        print("  \033[1;36mS  <SV2 file pathname>\033[0m   - \033[3mSave spreadsheet to file\033[0m")
        print("\033[1;33m[Edit]\033[0m")
        print("  \033[1;32mC\033[0m                      - \033[3mCreate a new spreadsheet\033[0m")
        print("  \033[1;32mE <cell> <content>\033[0m      - \033[3mEdit a cell\033[0m")
        print("\033[1;31mX\033[0m                      - \033[1mExit\033[0m")
        print("\033[1;4;36m==============================\033[0m")
        

        user_input = input("Enter command: ").strip()
        command = user_input[:2].upper() + user_input[2:]

        return command