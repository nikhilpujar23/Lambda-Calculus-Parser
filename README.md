
A lambda calculus Parser written in Python. Can be used by mathematicians.

## Execution

1. Clone this repository:

    ```
    gh repo clone nikhilpujar23/Lamda-Calculus-Parser
    ```

2. Move into the newly created directory:

    ```
    cd lambda-calculus-parser
    ```

3. To Run:

    ```
    python3 __main.py__
    ```

# Lambda Calculus Interpreter

This project is a lambda calculus interpreter implemented in Python, capable of parsing and evaluating expressions based on lambda calculus rules. The interpreter supports normal order reduction, syntactic analysis, and α-conversion to avoid variable capture.

## Grammar Specification

Lambda calculus expressions in this interpreter are defined by the following context-free grammar:

```
Expression -> Variable | Application | Abstraction
Variable -> ID
Application -> (Expression Expression)
Abstraction -> λID.Expression | @ID.Expression
```


- **Variable**: Represents identifiers.
- **Application**: Represents the application of one lambda expression to another.
- **Abstraction**: Defines an anonymous function with a bound variable and a body expression.

## Features

- **Normal Order Reduction**: Executes the outermost lambda expression first, displaying each reduction step.
- **Syntax Error Handling**: Provides user-friendly error messages for syntax errors.
- **Alpha Conversion**: Automatically renames variables during function application to prevent variable capture.

### Example Reductions


```
> (λm.((m λt.λf.t) λx.λt.λf.f) λz.λs.z)
((λz.λs.z λt.λf.t) λx.λt.λf.f)
(λs.λt.λf.t λx.λt.λf.f)
λt.λf.t
```

Syntax errors are nicely displayed to user:

```
> λx
ParseError: Expected: ., Found: EOF
```

During α-conversion, the interpreter has the capability to rename
variables to avoid variable capture:

```
> (λx.λy.(x y) y)
λa.(y a)
```


## Modules and Classes

### `lexer` Module

- **Lexer**: An iterator that tokenizes the source code into lambda calculus tokens.

### `parser` Module

- **Parser**: An LL(1) parser that performs syntactic analysis and constructs an abstract syntax tree (AST). Raises `ParserError` on syntax discrepancies.

### `lambda_calculus_ast` Module

- **Variable**, **Application**, **Abstraction**: Classes representing the nonterminals in the grammar. Each class is a subclass of `Expression`.

### `visitors` Module

- **FreeVariables**, **BoundVariables**: Visitors that compute the set of free or bound variables in an AST.
- **AlphaConversion**: Performs nondestructive substitution of all free occurrences of a variable with an expression.
- **BetaReduction**: Executes function application, providing a new AST with the applied reductions.



This README provides a comprehensive overview of your project and can be easily expanded or modified as your project grows. Adjust the repository URL and any specific installation instructions as necessary.cd

Contributors:
This is the major project sumission to NIT Jalandhar by:
Ketan Verma
Nikhil Pujar
Rajan Dhiman
Rajveer Singh
