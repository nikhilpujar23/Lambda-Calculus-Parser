import string

from collections import namedtuple

PUNCTUATION = ['λ', '@', '.', '(', ')']
WHITESPACE = list(string.whitespace)
Token = namedtuple('Token', ['type', 'value'])

class Lexer(object):
    """An iterator that splits lambda calculus source code into Tokens."""
    
    def __init__(self, source):
        self.source = source
        self.size = len(source)
        self.position = 0

    def __iter__(self):
        return self

    def __next__(self):
        self._clear_whitespace()
        if self.position >= self.size:
            raise StopIteration()
        current_char = self.source[self.position]

        # Handle numbers, including those with a decimal point
        if current_char.isdigit() or (current_char == '.' and self.position + 1 < self.size and self.source[self.position + 1].isdigit()):
            return self._number()

        # Handle punctuation and symbols
        if current_char in PUNCTUATION:
            self.position += 1
            return Token(current_char, None)
        
        # Handle symbols including function names
        return self._identify_function_or_symbol()

    def _number(self):
        start_pos = self.position
        has_decimal = False
        while self.position < self.size and (self.source[self.position].isdigit() or (self.source[self.position] == '.' and not has_decimal)):
            if self.source[self.position] == '.':
                has_decimal = True
            self.position += 1
        number_str = self.source[start_pos:self.position]
        return Token('NUMBER', float(number_str))

    def _identify_function_or_symbol(self):
        start_pos = self.position
        while (self.position < self.size and
               self.source[self.position] not in PUNCTUATION + WHITESPACE):
            self.position += 1
        symbol = self.source[start_pos:self.position]
        if symbol in {'sin', 'cos', 'exp'}:
            return Token(symbol.upper(), symbol)
        return Token('SYMBOL', symbol)

    def _clear_whitespace(self):
        while (self.position < self.size and
               self.source[self.position] in string.whitespace):
            self.position += 1
