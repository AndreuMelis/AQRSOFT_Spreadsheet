import os
import csv  
from spreadsheet.cell import Cell
from spreadsheet.coordinate import Coordinate
from spreadsheet.spreadsheet import Spreadsheet
from exceptions import (
    InvalidFileNameException,
    InvalidFilePathException,
    FileNotFoundException
)

class SaveFile:
    def __init__(self):
        pass

    def prompt_for_file_name(self, file_extension: str) -> str:
        file_name = input("Enter the file name: ").strip()
        file_name += file_extension
        return file_name

    def prompt_for_directory(self) -> str:
        directory_path = input("Enter the directory path: ").strip()
        return directory_path

    def validate_file_name(self, file_name: str):
        name, ext = os.path.splitext(file_name)
        if not name or ext.lower() not in ['.s2v', '.txt']:
            raise InvalidFileNameException(
                "Invalid file name or extension. Must be .s2v or .txt"
            )

    def validate_directory_path(self, directory_path: str):
        if not os.path.exists(directory_path):
            raise InvalidFilePathException("Directory does not exist.")

    def save_spreadsheet_data(self, file_name: str, directory_path: str, spreadsheet_data: list):
        try:
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'w', encoding='utf-8') as file:
                for row in spreadsheet_data:
                    file.write(';'.join(row) + '\n')
        except FileNotFoundError:
            raise FileNotFoundException("Unable to write to file: File not found.")
        except Exception as e:
            raise Exception(f"Unexpected error while saving: {e}")

    def display_save_confirmation(self):
        print("File saved successfully.")

    def _column_to_number(self, column: str) -> int:
        """Convert column letter(s) to number (A=1, B=2, ..., Z=26, AA=27, etc.)"""
        result = 0
        for char in column:
            result = result * 26 + (ord(char) - ord('A') + 1)
        return result

    def _number_to_column(self, num: int) -> str:
        """Convert number to column letter(s) (1=A, 2=B, ..., 26=Z, 27=AA, etc.)"""
        result = ""
        while num > 0:
            num -= 1
            result = chr(num % 26 + ord('A')) + result
            num //= 26
        return result

    def run_saver(self, spreadsheet):
        """Save the spreadsheet to a file."""
        # Get file details from user
        file_name = input("Enter the file name: ")
        directory_path = input("Enter the directory path: ")
        
        # Validate inputs
        self.validate_file_name(file_name)
        self.validate_directory_path(directory_path) 
        
        if not file_name.endswith('.s2v'):
            full_path = os.path.join(directory_path, file_name + ".s2v")
        else:
            full_path = os.path.join(directory_path, file_name)
        
        # Get bounds using the new List structure
        if not spreadsheet.cells:
            # Empty spreadsheet
            max_row = 0
            max_col_num = 0
        else:
            max_row = max((cell.coordinate.row for cell in spreadsheet.cells), default=0)
            max_col_num = max((self._column_to_number(cell.coordinate.column) for cell in spreadsheet.cells), default=0)
        
        # Create the data grid
        data = []
        for row in range(1, max_row + 1):
            row_data = []
            for col_num in range(1, max_col_num + 1):
                col_letter = self._number_to_column(col_num)
                
                # Find cell using the new List structure
                cell = spreadsheet.get_cell(Coordinate(col_letter, row))
                
                if cell:
                    # Get the cell's textual representation for saving
                    cell_content = cell.get_textual_representation()
                    row_data.append(cell_content)  
                else:
                    row_data.append("")  
            data.append(row_data)
        try:
            with open(full_path, 'w', newline='', encoding='utf-8') as file:
                for row in data:
                    line = ';'.join(row) + ';\n'  # Add semicolon after each value and at end
                    file.write(line)
            print(f"Spreadsheet saved to: {full_path}")
        except Exception as e:
            raise FileNotFoundException(f"Could not save file: {e}")