from enum import auto
from symtable import Symbol
from automata import *
from syntaxtree import *
from functools import reduce
from prepareER import *
from symbol_table import SymbolTable
class LexicalAnalyser():
    def __init__(self, language_path = "inputs/language.txt", automata_list = [], source = "inputs/source.txt"):
        self.language_path = language_path
        self.automata_list = automata_list
        self.NFA = None
        self.DFA = None
        self.source = source
        self.reservedKeys = []
        self.symbolTable = None
        self.identificators = None
        self.buildFinalAutomata()

    def buildFinalAutomata(self):
        patterns, reservedKeys, identificators, goesToSymbolTable = resolve_dependencies(self.language_path)
        self.reservedKeys = reservedKeys
        self.identificators = identificators
        self.goesToSymbolTable = goesToSymbolTable

        # Automatas are created in the order of the list of expressions
        for key, value in patterns.items():
            automata = SyntaxTree(value).getAutomata().toNFA()
            if key in identificators:
                for s in automata.final:
                    s.meaning = [key]
            self.automata_list.append(automata)

        for key, value in reservedKeys:
            automata = SyntaxTree(value).getAutomata().toNFA()
            for s in automata.final:
                s.meaning = [key]
            self.automata_list.append(automata)
            self.goesToSymbolTable.insert(0, key)
        
        self.reservedKeys = list(map(lambda x: x[0], self.reservedKeys))

        self.NFA = reduce(Automata.__add__, self.automata_list)
        self.DFA = self.NFA.toDFA()
        # Generate Symbol Table
        self.symbolTable = SymbolTable(self.reservedKeys)
        

    def tokenize(self):
        with open(self.source, "r") as file:
            lines = file.readlines()
        self.lexemes = []
        for line in lines:
            self.lexemes.extend(list(map(lambda x: [x[0], x[1].meaning], self.DFA.run(line))))
        self.tokens = []
        for lexeme, meaningList in self.lexemes:
            if len(set(meaningList).intersection(self.goesToSymbolTable)):
                l = self.symbolTable.lookup(lexeme)
                if not l:
                    for meaning in self.identificators:
                        if meaning in meaningList:
                            self.symbolTable.symbols.append([lexeme, meaning])
                            self.tokens.append([self.symbolTable.lookup(lexeme)[1], self.symbolTable.index(lexeme)])
                            break
                else:
                    if lexeme in self.reservedKeys:
                        self.tokens.append(l)
                    else:
                        self.tokens.append([l[1], self.symbolTable.index(lexeme)])
            else:
                for meaning in self.identificators:
                    if meaning in meaningList:
                        self.tokens.append([lexeme, meaning])
                        break
        return self.tokens

if __name__ == "__main__":
    lexical_analyzer = LexicalAnalyser("inputs/language.txt")
    automata_to_csv("outputs/csv_files/AutomatoLanguages.csv", lexical_analyzer.DFA, lexical_analyzer.DFA.listOfSymbols())
    csv_to_table("outputs/csv_files/AutomatoLanguages.csv", "outputs/table_result/AutomatoLanguages.csv")
    tokens = lexical_analyzer.tokenize()
    tokens_to_txt("outputs/tokens.txt", tokens)
    symbol_table_to_csv("outputs/symboltable.csv", lexical_analyzer.symbolTable.symbols)