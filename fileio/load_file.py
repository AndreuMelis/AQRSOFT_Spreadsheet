import os
import csv
from exceptions import (
    InvalidFilePathException,
    InvalidFileNameException,
    FileNotFoundException
)
from ui.display import DisplayContent


class LoadFile:
    def __init__(self):
        self.show = DisplayContent()

    def prompt_for_file_path(self) -> str:
        file_path = input("Enter the file path: ").strip()
        if not file_path:
            print("Invalid file path. Please provide a valid path.")
            return None
        return file_path

    def validate_file_format(self, file_path: str):
        if file_path is None:
            raise InvalidFilePathException("No path provided.")
        if not os.path.exists(file_path):
            raise FileNotFoundException(f"File does not exist: {file_path}")
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in ['.csv', '.txt', '.s2v']:
            raise InvalidFileNameException(f"Unsupported file format: {ext}")

    def load_spreadsheet_data(self, file_path: str) -> list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                return list(reader)
        except Exception as e:
            raise FileNotFoundException(f"Failed to read file: {e}")

    def run_loader(self):
        file_path = self.prompt_for_file_path()
        if file_path:
            try:
                self.validate_file_format(file_path)
                spreadsheet_data = self.load_spreadsheet_data(file_path)
                self.show.printContentSpreadsheet(spreadsheet_data)
            except (InvalidFilePathException, InvalidFileNameException, FileNotFoundException) as e:
                print(f"Error: {str(e)}")
        else:
            print("No file path provided. Aborting.")
