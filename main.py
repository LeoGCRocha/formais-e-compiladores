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
    for er in list_of_er:
        print("Expressão Regular: {}".format(er))
        syntax_tree = SyntaxTree(er)
        syntax_tree.printAutomata()
        automata_list.append(syntax_tree.getAutomata())
if __name__ == "__main__":
    erToAF("inputs/ertoaf.txt")