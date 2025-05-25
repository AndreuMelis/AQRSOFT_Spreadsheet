import os
from cell import Cell
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
            raise InvalidFileNameException("Invalid file name or extension. Must be .s2v or .txt")

    def validate_directory(self, directory_path: str):
        if not os.path.exists(directory_path):
            raise InvalidFilePathException("Directory does not exist.")

    def save_spreadsheet_data(self, file_name: str, directory_path: str, spreadsheet_data: list):
        try:
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'w', encoding='utf-8') as file:
                for row in spreadsheet_data:
                    file.write(';'.join(map(str, row)) + '\n')
        except FileNotFoundError:
            raise FileNotFoundException("Unable to write to file: File not found.")
        except Exception as e:
            raise Exception(f"Unexpected error while saving: {e}")

    def display_save_confirmation(self):
        print("File saved successfully.")

    def run_saver(self, spreadsheet):
        file_extension = ".s2v"
        file_name = self.prompt_for_file_name(file_extension)
        directory_path = self.prompt_for_directory()

        max_row = max(sorted(set(int(key[1:]) for key in spreadsheet.cells.keys() if key[1:].isdigit())), default=0)
        if file_name and directory_path:
            try:
                self.validate_file_name(file_name)
                self.validate_directory(directory_path)

                letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

                spreadsheet_data = [
                    [
                        str(spreadsheet.cells.get(f"{col}{row}", Cell()).content.get_value()).replace(";", ",") + ";"
                        for col in letters
                    ]
                    for row in range(1, max_row + 1)
                ]

                self.save_spreadsheet_data(file_name, directory_path, spreadsheet_data)
                self.display_save_confirmation()

            except (InvalidFileNameException, InvalidFilePathException, FileNotFoundException) as e:
                print(f"Error: {str(e)}")
