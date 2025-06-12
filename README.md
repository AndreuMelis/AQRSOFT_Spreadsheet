# AQRSOFT_Spreadsheet
Spreadsheet project in python
![App Screenshot](DCD_202500612_vFinal.png.png)

## Project Structure
```
AQRSOFT_Spreadsheet/
C:.
│   .DS_Store
│   DCD_20250612_vFinal.png.png
│   exceptions.py
│   main.py
│   README.md
│   test_RF
│   __init__.py
├───content
│   │   cell_content.py
│   │   formula_content.py
│   │   number.py
│   │   numerical_content.py
│   │   text_content.py
│   │   __init__.py
│
├───entities
│   │   bad_coordinate_exception.py
│   │   circular_dependency_exception.py
│   │   content_exception.py
│   │   no_number_exception.py
│   │   __init__.py
|
├───fileio
│   │   load_file.py
│   │   save_file.py
│   │   __init__.py
│
├───formula
│   │   formula_element.py
│   │   function.py
│   │   operand.py
│   │   operator.py
│   │   parser.py
│   │   postfix_converter.py
│   │   postfix_evaluator.py
│   │   tokenizer.py
│   │   __init__.py
│
├───markerrun
│   │   circular_dependencies_test.py
│   │   ClasesCorrector.py
│   │   dependent_cells_test.py
│   │   formula_content_test.py
│   │   load_test.py
│   │   marker_save_test.s2v
│   │   marker_save_test_ref.s2v
│   │   number_content_test.py
│   │   save_test.py
│   │   TestsRunner.py
│   │   text_content_test.py
│   │   __init__.py
│   
├───spreadsheet
│   │   cell.py
│   │   cell_range.py
│   │   coordinate.py
│   │   dependency_manager.py
│   │   spreadsheet.py
│   │   spreadsheet_controller.py
│   │   __init__.py
│   
├───ui
│   │   display.py
│   │   terminal_ui.py
│   │   __init__.py
|   
├───usecasesmarker
│   │   reading_spreadsheet_exception.py
│   │   saving_spreadsheet_exception.py
│   │   spreadsheet_controller_for_checker.py
│   │   spread_sheet_factory_for_checker.py
│   │   __init__.py
|____
```

- **`main.py`**: Run this file to start the spreadsheet application.
    ```bash
    python main.py
    ```

- **`TestsRunner.py`**: Run this file to execute all tests for the project.
    ```bash
    python markerrun/TestsRunner.py
    ```

Make sure you are in the `AQRSOFT_Spreadsheet` directory when running these commands.

## Getting Started

1. Clone or download the repository.
2. Navigate to the project folder.
3. Use the commands above to run the application or tests.