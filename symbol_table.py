import copy
from signal import raise_signal

class SymbolTable:
    # lexeme, meaning
    def __init__(self, symbols):
        self.symbols = [[symbol, symbol] for symbol in copy.deepcopy(symbols)]

    def lookup(self, lexeme):
        for l in self.symbols:
            if lexeme == l[0]:
                return l
        return []
    
    def index(self, lexeme):
        for i in range(len(self.symbols)):
            if self.symbols[i][0] == lexeme:
                return i
        raise(Exception("lexeme not found in symbol table"))