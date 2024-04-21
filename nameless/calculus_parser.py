from lambda_calculus_ast import Variable, Application, Abstraction, Sin, Cos, Exp, Number

class Parser(object):
    """An LL(1) parser that performs syntactic analysis on lambda calculus source code."""
    
    def __init__(self, lexer):
        self.lexer = lexer
        self.token = next(self.lexer)
    
    def parse(self):
        """Returns an abstract syntax tree if the source correctly fits the rules of lambda calculus."""
        return self._expression()
    
    def _error(self, expected):
        """Raises a ParserError for token mismatches."""
        raise ParserError(expected, self.token.type)
    
    def _advance(self):
        """Moves to the next token, handling the end of stream safely."""
        try:
            self.token = next(self.lexer)
        except StopIteration:
            self.token = None  # Or consider a special EOF token, based on your design

    
    def _eat(self, prediction):
        """Consumes a token if it matches the prediction, otherwise raises an error."""
        if self.token.type == prediction:
            self._advance()
        else:
            self._error("Expected: {}, Found: {}".format(prediction, self.token.type))
    
    def _expression(self):
        if self.token.type == '(':
            self._advance()
            exprs = []
            while self.token and self.token.type != ')':
                exprs.append(self._expression())
            self._eat(')')
            # Process the list of expressions according to your language's semantics (e.g., function application)
            return self._process_application(exprs)
        elif self.token.type in ['λ', '@']:
            return self._abstraction()
        elif self.token.type == 'SYMBOL' or self.token.type in ['SIN', 'COS', 'EXP']:
            return self._function_or_variable()
        elif self.token.type == 'NUMBER':
            num = self.token.value
            self._advance()
            return Number(num)
        else:
            self._error("Expected expression")

    def _process_application(self, exprs):
        # Assuming left-associative function application
        result = exprs[0]
        for expr in exprs[1:]:
            result = Application(result, expr)
        return result

    
    def _function_or_variable(self):
        """Handles function or variable expressions based on the current token."""
        if self.token.type == 'SYMBOL':
            return self._variable()
        else:
            return self._math_function()
    
    def _variable(self):
        """Handles variable expressions."""
        name = self.token.value
        self._advance()
        return Variable(name)
    
    def _application(self):
        """Handles application expressions."""
        self._eat('(')
        left_expression = self._expression()
        right_expression = self._expression()
        self._eat(')')
        return Application(left_expression, right_expression)
    
    def _abstraction(self):
        self._eat('λ')  # Consume the lambda token
        if self.token.type != 'SYMBOL':
            self._error("Expected variable after 'λ'")
        variable = self.token.value
        self._advance()
        self._eat('.')  # Consume the dot that separates the head from the body
        body = self._expression()  # Recursively parse the body
        return Abstraction(Variable(variable), body)

    def _math_function(self):
        """Handles mathematical functions with their arguments."""
        func_name = self.token.value.lower()
        self._advance()  # move past the function name
        self._eat('(')  # ensure that a '(' follows the function name
        argument = self._expression()  # get the argument
        self._eat(')')  # ensure closing ')'
        if func_name == 'sin':
            return Sin(argument)
        elif func_name == 'cos':
            return Cos(argument)
        elif func_name == 'exp':
            return Exp(argument)

class ParserError(Exception):
    """Exception for parsing errors."""
    
    def __init__(self, expected, found):
        super().__init__(f'Expected: {expected}, Found: {found}')
        self.expected = expected
        self.found = found
