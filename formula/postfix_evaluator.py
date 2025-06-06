# --------------------------------------------------------------------------------------------------
# Archivo: formula/postfix_evaluator.py
# --------------------------------------------------------------------------------------------------

from typing import List, Union, Any
from exceptions import EvaluationErrorException, InvalidPostfixException

# Importamos las bases de visitor y elemento desde formula_element
from .formula_element import FormulaElementVisitor, FormulaElement
from .operand import Operand
from .operator import Operator
from .function import Function, FunctionArgument


class PostfixEvaluationVisitor(FormulaElementVisitor):
    """
    Implementación de FormulaElementVisitor que evalúa una expresión en notación postfix.
    Mantiene una pila interna de valores numéricos.
    """
    
    def __init__(self):
        self.evaluation_stack: List[Union[int, float]] = []
    
    def visit_operator(self, operator: Operator):
        if len(self.evaluation_stack) < 2:
            raise InvalidPostfixException(
                f"Not enough operands for operator '{operator.type}'"
            )
        right = self.evaluation_stack.pop()
        left = self.evaluation_stack.pop()
        result = self._perform_operation(operator.type, left, right)
        self.evaluation_stack.append(result)
    
    def visit_operand(self, operand: Operand):
        """Procesa un operando empujando su valor en la pila."""
        value = operand.get_value()
        self.evaluation_stack.append(value)
    
    def visit_function(self, function_element: Function):
        """Procesa una función evaluando sus argumentos y llamando a la función."""
        try:
            argument_values: List[Union[int, float]] = []
            for arg in function_element.arguments:
                if isinstance(arg, FunctionArgument):
                    value = arg.get_value(function_element.spreadsheet)
                    if isinstance(value, list):
                        argument_values.extend(value)
                    else:
                        argument_values.append(value)
                else:
                    argument_values.append(arg)

            result = self._evaluate_function(function_element, argument_values)
            self.evaluation_stack.append(result)

        except Exception as e:
            raise EvaluationErrorException(f"Function evaluation failed: {str(e)}")
    
    def _perform_operation(
        self,
        operator_type: str,
        left: Union[int, float],
        right: Union[int, float]
    ) -> Union[int, float]:
        """Ejecuta la operación aritmética según el tipo de operador."""
        if operator_type == '+':
            return left + right
        elif operator_type == '-':
            return left - right
        elif operator_type == '*':
            return left * right
        elif operator_type == '/':
            if right == 0:
                raise EvaluationErrorException("Division by zero")
            return left / right
        else:
            raise EvaluationErrorException(f"Unsupported operator: {operator_type}")
    
    def _evaluate_function(
        self,
        function_instance: Function,
        arguments: List[Union[int, float]]
    ) -> Union[int, float]:
        """Invoca `function_instance.evaluate` con los argumentos dados."""
        try:
            return function_instance.evaluate(arguments)
        except Exception as e:
            raise EvaluationErrorException(f"Function evaluation failed: {str(e)}")


class PostfixExpressionEvaluator:
    """Clase principal para evaluar una lista de elementos en orden postfix."""
    
    def evaluate_postfix_expression(
        self,
        postfix_expression: List[FormulaElement],
    ) -> Union[int, float]:
        """
        Evalúa una expresión en postfix y devuelve el resultado numérico.
        """
        if not postfix_expression:
            raise InvalidPostfixException("Empty postfix expression")
        
        visitor = PostfixEvaluationVisitor()
        
        for element in postfix_expression:
            element.accept(visitor)
        
        if len(visitor.evaluation_stack) != 1:
            raise InvalidPostfixException(
                f"Invalid postfix expression: expected 1 result, got {len(visitor.evaluation_stack)}"
            )
        
        return visitor.evaluation_stack[0]
