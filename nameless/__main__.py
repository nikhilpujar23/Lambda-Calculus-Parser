from lexer import Lexer
from calculus_parser import Parser, ParserError
from visitors import BetaReduction

def interpret(input_string, print_reductions=False):
    """Performs normal order reduction on the given string lambda calculus expression."""
    lexer = Lexer(input_string)
    try:
        ast = Parser(lexer).parse()
    except ParserError as discrepancy:
        print('ParseError:', discrepancy)
        return None
    normal_form = False
    while not normal_form:
        reducer = BetaReduction()
        reduced_ast = reducer.visit(ast)
        normal_form = not reducer.reduced
        if print_reductions:
            print('Reduction step:', str(ast))
        ast = reduced_ast
    return str(ast)

def main():
    """Begins an interactive lambda calculus interpreter with support for mathematical functions."""
    print("Welcome to the Lambda Calculus Interpreter with Extensions!\n"
          "Type 'quit' to exit.\n"
          "You can now use 'sin', 'cos', and 'exp' functions, e.g., sin(0.5), cos(x), exp(λx.x).")
    while True:
        read = input('> ')
        if read == 'quit':
            break
        if read:
            result = interpret(read, print_reductions=True)
            if result is not None:
                print('Result:', result)

if __name__ == '__main__':
    main()
