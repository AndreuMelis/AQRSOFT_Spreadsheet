from postfix_evaluator import FormulaElementVisitor, FormulaElement

class Operator(FormulaElement):
    """Represents mathematical operators in formulas"""
    
    def __init__(self, operator_type: str) -> None:
        self.type: str = operator_type

    def accept(self, visitor: FormulaElementVisitor) -> Any:
        return visitor.visit_operator(self)

class OperatorEvaluator:
    def __init__(self):
        pass