class Expression(object):
    """Abstract class for any lambda calculus expression."""
    _fields = ()  # No fields because this is an abstract base class

    def children(self):
        """Returns a list of Expression objects."""
        pass

class Variable(Expression):
    """Encapsulates a lambda calculus variable."""
    _fields = ('name',)  # No children, just the name

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def children(self):
        return []

class Application(Expression):
    """Encapsulates a lambda calculus function call."""
    _fields = ('left_expression', 'right_expression')

    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression

    def __str__(self):
        return '({} {})'.format(self.left_expression, self.right_expression)

    def children(self):
        return [self.left_expression, self.right_expression]

class Abstraction(Expression):
    """Encapsulates a function in lambda calculus."""
    _fields = ('parameter', 'body')

    def __init__(self, parameter, body):
        self.parameter = parameter
        self.body = body

    def __str__(self):
        return 'λ{}.{}'.format(self.parameter, self.body)

    def children(self):
        return [self.parameter, self.body]

class Sin(Expression):
    """Represents the sine function applied to an argument."""
    _fields = ('argument',)

    def __init__(self, argument):
        self.argument = argument

    def __str__(self):
        return 'sin({})'.format(self.argument)

    def children(self):
        return [self.argument]

class Cos(Expression):
    """Represents the cosine function applied to an argument."""
    _fields = ('argument',)

    def __init__(self, argument):
        self.argument = argument

    def __str__(self):
        return 'cos({})'.format(self.argument)

    def children(self):
        return [self.argument]

class Exp(Expression):
    """Represents the exponential function applied to an argument."""
    _fields = ('argument',)

    def __init__(self, argument):
        self.argument = argument

    def __str__(self):
        return 'exp({})'.format(self.argument)

    def children(self):
        return [self.argument]

class Number(Expression):
    """Represents a numeric value."""
    _fields = ('value',)

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def children(self):
        return []
