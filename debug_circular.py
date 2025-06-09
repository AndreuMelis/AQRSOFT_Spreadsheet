from usecasesmarker.spreadsheet_controller_for_checker import ISpreadsheetControllerForChecker
import exceptions as ex

controller = ISpreadsheetControllerForChecker()

print("Step 1: Setting A1 = =A2+A3+A4+A5")
controller.set_cell_content("A1", "=A2+A3+A4+A5")
print("✓ A1 set successfully")

print("Step 2: About to set A2 = =A1+A7+A8")
try:
    controller.set_cell_content("A2", "=A1+A7+A8")
    print("✓ A2 set successfully - NO EXCEPTION")
    
    # Maybe exception happens during evaluation?
    print("Step 3: Trying to get A1 value...")
    val = controller.get_cell_content_as_float("A1")
    print(f"A1 value: {val}")
    
    print("Step 4: Trying to get A2 value...")
    val = controller.get_cell_content_as_float("A2")
    print(f"A2 value: {val}")
    
except ex.CircularDependencyException as e:
    print(f"✓ CircularDependencyException during set_cell_content: {e}")
except Exception as e:
    print(f"✗ Other exception during set_cell_content: {type(e).__name__}: {e}")