# usecasesmarker/spread_sheet_factory_for_checker.py

from usecasesmarker.spreadsheet_controller_for_checker import ISpreadsheetControllerForChecker

class SpreadSheetFactoryForChecker:
    @staticmethod
    def create_spreadsheet_controller():
        """
        Must return an object that implements all methods of
        ISpreadsheetControllerForChecker (set_cell_content, etc.)
        """
        return ISpreadsheetControllerForChecker()
