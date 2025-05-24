from content.cell_content import CellContent
from abc import ABC, abstractmethod
from formula.tokenizer   import Tokenizer
from formula.parser      import Parser
from formula.infix_to_postfix import InfixToPostfixConverter
from formula.postfix_evaluator   import PostfixExpressionEvaluator

# FormulaContent (hooks into tokenizer/parser/evaluator)
class FormulaContent(CellContent):
    def __init__(self, formula: str) -> None:
        super().__init__()
        self.formula = formula

    def get_value(self, spreadsheet):
        # 1) tokenize
        # 2) parse/check syntax
        # 3) convert to postfix
        # 4) evaluate
        # (all delegated to formula/ modules)
        

        tokens     = Tokenizer().tokenize(self.formula)
        Parser(tokens).parse()
        postfix    = InfixToPostfixConverter().to_postfix(tokens)
        result     = PostfixExpressionEvaluator().evaluate_postfix_expression(postfix, spreadsheet)
        return result
