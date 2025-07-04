from spreadsheet.cell_range import CellRange
from spreadsheet.spreadsheet import Spreadsheet

class DisplayContent:

    def __init__(self):
        pass

    def printContentSpreadsheet(self, spreadsheet_data):
        if not spreadsheet_data:
            print("No data to display.")
            return

        for row in spreadsheet_data:
            for cell_data in row:
                print(cell_data.replace(';', '\t'), end='\t')
            print()