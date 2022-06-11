from enum import auto
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
        dependencies = resolve_dependencies(self.language_path)
        list_of_expressions = dependencies[0]
        self.reservedKeys = dependencies[1]
        self.identificators = dependencies[2]
        print(self.reservedKeys)
        print(self.identificators)
        # Automatas are created in the order of the list of expressions
        for key, value in list_of_expressions.items():
            automata = SyntaxTree(value).getAutomata().toNFA()
            for s in automata.final:
                s.meaning = [key]
            self.automata_list.append(automata) 
        result = reduce(Automata.__add__, self.automata_list)
        self.NFA = result
        self.DFA = self.NFA.toDFA()
        # Generate Symbol Table
        self.symbolTable = SymbolTable(self.reservedKeys)
        # Read Language and Generated Symbols
        self.prepare_symbol_table()
    def prepare_symbol_table(self):
        with open(self.source, "r") as file:
            lines = file.readlines()
            for line in lines:
                lexemeStates = self.DFA.run(line)
                print(lexemeStates)
if __name__ == "__main__":
    lexical_analyzer = LexicalAnalyser("inputs/language.txt")
    automata_to_csv("outputs/csv_files/AutomatoLanguages.csv", lexical_analyzer.DFA, lexical_analyzer.DFA.listOfSymbols())
    csv_to_table("outputs/csv_files/AutomatoLanguages.csv", "outputs/table_result/AutomatoLanguages.csv")