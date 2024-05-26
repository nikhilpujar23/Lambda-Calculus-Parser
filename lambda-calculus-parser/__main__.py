import streamlit as st
from streamlit_option_menu import option_menu
from lexer import Lexer
from calculus_parser import Parser, ParserError
from visitors import BetaReduction

# Members details
members = {
    "Ketan Verma": {
        "LinkedIn": "https://www.linkedin.com/in/ketan-verma-51717a242?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app ",
        "GitHub": "https://github.com/ketanvermaketan",
    },
    "Nikhil Pujar": {
        "LinkedIn": "https://www.linkedin.com/in/nikhil-pujar/",
        "GitHub": "https://github.com/nikhilpujar23",
    },
    "Rajan Dhiman": {
        "LinkedIn": "https://www.linkedin.com/in/rajan-dhiman-2a070920b/",
        "GitHub": "https://github.com/Rajancoding597",
    },
    "Rajveer Hayer": {
        "LinkedIn": "https://www.linkedin.com/in/rajveer-singh-021b63201/ ",
        "GitHub": "https://github.com/RajveerHayer09",
    }
}

def interpret(input_string, print_reductions=False):
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

    # Navbar
    with st.sidebar:
        # Add the logo above the menu bar
        st.sidebar.image("OIG3.jpg", use_column_width=True)

        selected = option_menu(
            "Menu",
            ["Interpreter", "Contact US"],
            icons=["code", "people"],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Interpreter":
        st.title("Lambda Calculus Interpreter")

        # Input field
        user_input = st.text_area("Enter a lambda calculus expression:")

        # Button to trigger action
        if st.button("Interpret"):
            # Call interpret function with user input
            result = interpret(user_input, print_reductions=True)
            if result is not None:
                st.success("Result: {}".format(result))
    else:
        st.title("Contact US")

        for member, accounts in members.items():
            st.write(f"## {member}")
            st.write("### Media Accounts:")
            for platform, link in accounts.items():
                st.write(f"[{platform}]({link})")
            st.write("---")

    st.sidebar.title("About")
    st.sidebar.info("""
        This application provides a Lambda Calculus Interpreter and details about the project members.
        Use the menu to switch between the interpreter and member details.
    """)

if __name__ == '__main__':
    main()
