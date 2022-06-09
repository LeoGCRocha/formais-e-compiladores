from enum import auto
from automata import *
from syntaxtree import *
from functools import reduce
from prepareER import *
class LexicalAnalyser():
    def __init__(self, language_path = "inputs/language.txt", automata_list = []):
        self.language_path = language_path
        self.automata_list = automata_list
        self.NFA = None
        self.DFA = None
        self.buildFinalAutomata()
    def buildFinalAutomata(self):
        list_of_expressions = resolve_dependencies(self.language_path)
        # Automatas are created in the order of the list of expressions
        for key, value in list_of_expressions.items():
            # print(value)
            automata = SyntaxTree(value).getAutomata().toNFA()
            for s in automata.final:
                s.meaning = [key]
            self.automata_list.append(automata)
        result = reduce(Automata.__add__, self.automata_list)
        self.NFA = result
        self.DFA = self.NFA.toDFA()

if __name__ == "__main__":
    lexical_analyzer = LexicalAnalyser("inputs/language.txt")
    automata_to_csv("outputs/csv_files/AutomatoLanguages.csv", lexical_analyzer.DFA, lexical_analyzer.DFA.listOfSymbols())
    csv_to_table("outputs/csv_files/AutomatoLanguages.csv", "outputs/table_result/AutomatoLanguages.csv")