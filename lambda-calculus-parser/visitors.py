import ast
import itertools
import math

from lambda_calculus_ast import Variable, Application, Abstraction, Sin, Cos, Exp,Number

class FreeVariables(ast.NodeVisitor):
    """Finds unbound variables in a lambda calculus AST."""
    def visit_Variable(self, node):
        return {node.name}

    def visit_Application(self, node):
        return self.visit(node.left_expression) | self.visit(node.right_expression)

    def visit_Abstraction(self, node):
        return self.visit(node.body) - {node.parameter.name}

    def visit_Sin(self, node):
        return self.visit(node.argument)

    def visit_Cos(self, node):
        return self.visit(node.argument)

    def visit_Exp(self, node):
        return self.visit(node.argument)

class BoundVariables(ast.NodeVisitor):
    """Finds bound variables in a lambda calculus AST."""
    def visit_Variable(self, node):
        return set()

    def visit_Application(self, node):
        return self.visit(node.left_expression) | self.visit(node.right_expression)

    def visit_Abstraction(self, node):
        return self.visit(node.body) | {node.parameter.name}

    def visit_Sin(self, node):
        return self.visit(node.argument)

    def visit_Cos(self, node):
        return self.visit(node.argument)

    def visit_Exp(self, node):
        return self.visit(node.argument)

class AlphaConversion(ast.NodeVisitor):
    """Substitutes free occurrences of variables."""
    def __init__(self, to_replace, replacement):
        self.to_replace = to_replace
        self.replacement = replacement

    def visit_Variable(self, node):
        if node.name == self.to_replace.name:
            return self.replacement
        else:
            return Variable(node.name)

    def visit_Application(self, node):
        return Application(self.visit(node.left_expression), self.visit(node.right_expression))

    def visit_Abstraction(self, node):
        if node.parameter.name in FreeVariables().visit(self.replacement):
            unavailable_names = FreeVariables().visit(node) | {node.parameter.name}
            new_name = next(s for s in lexicographical() if s not in unavailable_names)
            new_parameter = Variable(new_name)
            converter = AlphaConversion(node.parameter, new_parameter)
            new_body = converter.visit(node.body)
            return Abstraction(new_parameter, self.visit(new_body))
        else:
            return Abstraction(self.visit(node.parameter), self.visit(node.body))

    def visit_Sin(self, node):
        return Sin(self.visit(node.argument))

    def visit_Cos(self, node):
        return Cos(self.visit(node.argument))

    def visit_Exp(self, node):
        return Exp(self.visit(node.argument))

def lexicographical():
    """Generates all alphabetic strings in lexicographical order."""
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for size in itertools.count(1):
        for string in itertools.product(alphabet, repeat=size):
            yield ''.join(string)

class BetaReduction(ast.NodeVisitor):
    """Performs beta reduction in a lambda calculus AST."""
    def __init__(self):
        self.reduced = False

    def visit_Variable(self, node):
        # Assuming you have some mechanism to resolve variables
        return Variable(node.name)

    def visit_Application(self, node):
        if isinstance(node.left_expression, Abstraction) and not self.reduced:
            self.reduced = True
            converter = AlphaConversion(node.left_expression.parameter, node.right_expression)
            return converter.visit(node.left_expression.body)
        else:
            return Application(self.visit(node.left_expression), self.visit(node.right_expression))

    def visit_Abstraction(self, node):
        return Abstraction(self.visit(node.parameter), self.visit(node.body))
    
    def visit_Sin(self, node):
        argument = self.visit(node.argument)  # Evaluate the argument
        if argument is None:
            raise ValueError("Argument to sin() is None, which suggests an evaluation issue.")

        if isinstance(argument, Number):  # Ensure the argument is a Number instance
            return math.sin(argument.value)
        elif isinstance(argument, (int, float)):  # Handle Python primitives if bypassing Number
            return math.sin(argument)
        else:
            raise TypeError(f"sin function expects a numeric value, got {type(argument).__name__}")

    def visit_Number(self, node):
        print(f"Visiting Number: {node.value}")
        return node.value

    def visit_Cos(self, node):
        argument = self.visit(node.argument)
        if argument is None:
            raise ValueError("Argument to cos() is None, which suggests an evaluation issue.")

        if isinstance(argument, Number):  # Ensure the argument is a Number instance
            return math.cos(argument.value)
        elif isinstance(argument, (int, float)):  # Handle Python primitives if bypassing Number
            return math.cos(argument)
        else:
            raise TypeError(f"cos function expects a numeric value, got {type(argument).__name__}")

    def visit_Exp(self, node):
        argument = self.visit(node.argument)
        if argument is None:
            raise ValueError("Argument to exp() is None, which suggests an evaluation issue.")

        if isinstance(argument, Number):  # Ensure the argument is a Number instance
            return math.exp(argument.value)
        elif isinstance(argument, (int, float)):  # Handle Python primitives if bypassing Number
            return math.exp(argument)
        else:
            raise TypeError(f"exp function expects a numeric value, got {type(argument).__name__}")
