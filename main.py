from spreadsheet.spreadsheet import Spreadsheet
from ui import TerminalUI

if __name__ == "__main__":

    spreadsheet = Spreadsheet()
    ui = TerminalUI(spreadsheet)
    ui.run()

