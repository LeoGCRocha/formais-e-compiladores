from utils import *
from prepareER import *
from automata import *
from syntaxtree import SyntaxTree
from lexical_analyser import *
import os
import glob
from files import *


if __name__ == "__main__":
    files = glob.glob("outputs/csv_files/*.csv")
    for f in files:
        os.remove(f)
    
    files = glob.glob("outputs/table_result/*.csv")
    for f in files:
        os.remove(f)

    # 1) Conversao de Expressao Regular para AF
    erToAF(Files.INPUT)
    # 2) Conversao de Automato Finito Nao Deterministico para Automato Finito Deterministico
    automata = t1()
    automata_to_csv(Files.CSV_1, automata, automata.listOfSymbols())
    csv_to_table(Files.CSV_1, Files.TABLE_1)
    
    automata = t2()
    automata_to_csv(Files.CSV_2, automata, automata.listOfSymbols())
    csv_to_table(Files.CSV_2, Files.TABLE_2)
    
    automata = t3()
    automata_to_csv(Files.CSV_3, automata, automata.listOfSymbols())
    csv_to_table(Files.CSV_3, Files.TABLE_3)

    automata = t4()
    automata_to_csv(Files.CSV_4, automata, automata.listOfSymbols())
    csv_to_table(Files.CSV_4, Files.TABLE_4)

    lexical_analyzer = LexicalAnalyser("inputs/language.txt")
    automata_to_csv("outputs/csv_files/AutomatoLanguages.csv", lexical_analyzer.DFA, lexical_analyzer.DFA.listOfSymbols())
    csv_to_table("outputs/csv_files/AutomatoLanguages.csv", "outputs/table_result/AutomatoLanguages.csv")
    tokens = lexical_analyzer.tokenize()
    tokens_to_txt("outputs/tokens.txt", tokens)
    symbol_table_to_csv("outputs/symboltable.csv", lexical_analyzer.symbolTable.symbols)