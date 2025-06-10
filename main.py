from spreadsheet.spreadsheet import Spreadsheet
from spreadsheet.spreadsheet_controller import SpreadsheetController

if __name__ == "__main__":

    spreadsheet = Spreadsheet()
    spreadsheet_controller = SpreadsheetController(spreadsheet)
    spreadsheet_controller.run_menu()
