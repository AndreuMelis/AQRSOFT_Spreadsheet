from exceptions import InvalidPostfixException
from typing import List, Union
from formula.operand import Operand
from formula.operator import Operator

class PostfixConverter:
    def __init__(self):
        # Define operator precedence (higher number = higher precedence)
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '^': 3,  # exponentiation
            '**': 3  # alternative exponentiation
        }
        
        # Define operator associativity (True = left-associative, False = right-associative)
        self.associativity = {
            '+': True,
            '-': True,
            '*': True,
            '/': True,
            '^': False,  # right-associative
            '**': False  # right-associative
        }

    def convert_to_postfix(self, tokens: List[Union[Operand, Operator]]) -> List[Union[Operand, Operator]]:
        """
        Convert infix token list to postfix (RPN) list using the Shunting-Yard Algorithm
        
        Args:
            tokens: List of Operand and Operator objects in infix notation
            
        Returns:
            List of tokens in postfix notation
            
        Raises:
            InvalidPostfixException: If the expression is malformed
        """
        if not tokens:
            raise InvalidPostfixException("Empty token list provided")
            
        output_queue = []  # Final postfix expression
        operator_stack = []  # Temporary stack for operators and parentheses
        
        try:
            for token in tokens:
                if isinstance(token, Operand):
                    # If token is an operand, add it to output queue
                    output_queue.append(token)
                    
                elif isinstance(token, Operator):
                    operator_symbol = token.get_symbol() 
                    
                    if operator_symbol == '(':
                        # Left parenthesis goes on stack
                        operator_stack.append(token)
                        
                    elif operator_symbol == ')':
                        # Right parenthesis: pop operators until left parenthesis
                        found_left_paren = False
                        while operator_stack:
                            top_operator = operator_stack.pop()
                            if isinstance(top_operator, Operator) and top_operator.get_symbol() == '(':
                                found_left_paren = True
                                break
                            output_queue.append(top_operator)
                        
                        if not found_left_paren:
                            raise InvalidPostfixException("Mismatched parentheses: missing left parenthesis")
                            
                    elif operator_symbol in self.precedence:
                        # Regular operator: handle precedence and associativity
                        while (operator_stack and 
                               isinstance(operator_stack[-1], Operator) and
                               operator_stack[-1].get_symbol() != '(' and
                               self._should_pop_operator(operator_symbol, operator_stack[-1].get_symbol())):
                            output_queue.append(operator_stack.pop())
                        
                        operator_stack.append(token)
                    else:
                        raise InvalidPostfixException(f"Unknown operator: {operator_symbol}")
                else:
                    raise InvalidPostfixException(f"Invalid token type: {type(token)}")
            
            # Pop remaining operators from stack
            while operator_stack:
                top_operator = operator_stack.pop()
                if isinstance(top_operator, Operator) and top_operator.get_symbol() in ['(', ')']:
                    raise InvalidPostfixException("Mismatched parentheses")
                output_queue.append(top_operator)
                
        except Exception as e:
            if isinstance(e, InvalidPostfixException):
                raise
            else:
                raise InvalidPostfixException(f"Error during postfix conversion: {str(e)}")
        
        if not output_queue:
            raise InvalidPostfixException("Conversion resulted in empty expression")
            
        return output_queue
    
    def _should_pop_operator(self, current_op: str, stack_top_op: str) -> bool:
        """
        Determine if the operator on top of stack should be popped based on precedence and associativity
        
        Args:
            current_op: Current operator being processed
            stack_top_op: Operator on top of the stack
            
        Returns:
            True if stack operator should be popped, False otherwise
        """
        if stack_top_op not in self.precedence:
            return False
            
        current_precedence = self.precedence[current_op]
        stack_precedence = self.precedence[stack_top_op]
        
        # Pop if stack operator has higher precedence
        if stack_precedence > current_precedence:
            return True
            
        # Pop if same precedence and current operator is left-associative
        if (stack_precedence == current_precedence and 
            self.associativity.get(current_op, True)):  # Default to left-associative
            return True
            
        return False
    
    def get_precedence(self, operator: str) -> int:
        """
        Get precedence value for an operator
        
        Args:
            operator: Operator symbol
            
        Returns:
            Precedence value (higher = higher precedence)
        """
        return self.precedence.get(operator, 0)
    
    def is_left_associative(self, operator: str) -> bool:
        """
        Check if operator is left-associative
        
        Args:
            operator: Operator symbol
            
        Returns:
            True if left-associative, False if right-associative
        """
        return self.associativity.get(operator, True)
