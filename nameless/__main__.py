from lexer import Lexer
from calculus_parser import Parser, ParserError
from visitors import BetaReduction
import streamlit as st
def interpret(input_string, print_reductions=False):
    """Performs normal order reduction on the given string lambda calculus expression."""
    """Performs normal order reduction on the given string lambda calculus expression."""
    lexer = Lexer(input_string)
    try:
        ast = Parser(lexer).parse()
    except ParserError as discrepancy:
        st.error('ParseError: {}'.format(discrepancy))
        return None
    normal_form = False
    while not normal_form:
        reducer = BetaReduction()
        reduced_ast = reducer.visit(ast)
        normal_form = not reducer.reduced
        if print_reductions:
            st.write('Reduction step:', str(ast))
        ast = reduced_ast
    return str(ast)

def main():
    st.set_page_config(page_title="Lambda Calculus Interpreter", page_icon=":smiley:")
    st.title("Lambda Calculus Interpreter")

    # Input field
    user_input = st.text_area("Enter a lambda calculus expression:")

    # Button to trigger action
    if st.button("Interpret"):
        # Call interpret function with user input
        result = interpret(user_input, print_reductions=True)
        if result is not None:
            st.success("Result: {}".format(result))

if __name__ == '__main__':
    main()
