from utils import *
from prepareER import *
from automata import Automata
from syntaxtree import SyntaxTree
# Receive a list of regular expressions from a single file
# and create multiples .csv with the respectives ER as Automatas
def erToAF(file_path):
    # Create a list of regular expressions
    list_of_er = read_er(file_path)
    list_of_er = list(map(lambda x: prepare_expression(x), list_of_er))
    for er in list_of_er:
        err = "A expressao {}, nao eh valida.".format(er)
        assert(verify_expression(er)), err
    # Create a list of automata
    automata_list = []
    number = 0
    for er in list_of_er:
        syntax_tree = SyntaxTree(er)
        automata_list.append(syntax_tree.getAutomata())
        # Save automata on .csv file
        file_path = "output/automata{}.csv".format(str(number))
        automata_to_csv(file_path, automata_list[-1], syntax_tree.getListOfSymbols())
        number += 1

if __name__ == "__main__":
    # 1) Conversao de Expressao Regular para AF
    # erToAF("inputs/ertoaf.txt")
    # 2) Conversao de Automato Finito Nao Deterministico para Automato Finito Deterministico