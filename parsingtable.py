import string
from copy import deepcopy
from operators import Operators as OP

#sentencas = {'S': [['A', 'k', 'O']], 'A': [['a', "A''"]], "A''": [['B', "A'"], [
#    'C', "A'"]], 'C': [['c']], 'B': [['b', 'B', 'C'], ['r']], "A'": [['d', "A'"], ['&']]}
#first_list = {'S': {'a'}, 'A': {'a'}, "A''": {'r', 'b', 'c'},
#              'C': {'c'}, 'B': {'r', 'b'}, "A'": {'&', 'd'}}
#follow_list = {'S': {'$'}, 'A': {'k'}, "A''": {'k'}, 'C': {
#    'k', 'd', 'c'}, 'B': {'k', 'd', 'c'}, "A'": {'k'}}
#terminals = ['k', 'O', 'd', 'a', 'c', 'b', 'r']
#non_terminals = ["S", "A", "A''", "C", "B", "A'"]
#terminals.append('$')

#sentencas = {'E': [['T', "E'"]], "E'": [['+', "T", "E'"],['&']], "T": [['F', "T"]],"T'": [['*', "F", "T'"],['&']],"F": [['(', "E", ")"],['id']]}
#first_list = {'E': {'(','id'}, "E'": {'+','&'}, "T": {'(', 'id'}, "T'": {'*',"&"}, "F": {'(', 'id'}}
#follow_list = {'E': {'$',')'}, "E'": {'$',')'}, "T": {'+', '$',')'}, "T'": {'+', '$',')'}, "F": {'*', '+','$', ')'}}
#terminals = ['id', '+', '*', '(', ')', '$']
#non_terminals = ['E',"E'","T","T'","F"]

sentencas = {'E': [['T', "E'"]], "E'": [['or', "T", "E'"],['&']], "T": [['F', "T'"]],"T'": [['and', "F", "T'"],['&']],"F": [['¬', "F"],['id']]}
first_list = {'E': {'¬','id'}, "E'": {'&','or'}, "T": {'¬', 'id'}, "T'": {'and',"&"}, "F": {'¬', 'id'}}
follow_list = {'E': {'$'}, "E'": {'$'}, "T": {'$', 'or'}, "T'": {'$', 'or'}, "F": {'and', '$', 'or'}}
terminals = ['id', 'or', 'and', '¬', '$']
non_terminals = ['E',"E'","T","T'","F"]

def generate_parse_table(terminals, non_terminals, grammar, grammar_first, grammar_follow):
    parse_table = [["-"]*len(terminals) for i in range(len(non_terminals))]
    grammar2 = deepcopy(grammar)

    for non_terminal, expression in grammar.items():
        #print(non_terminal, expression)
        #print("primeiro caracter expressao é %s" % expression[0][0])
        # print({non_terminal:grammar[non_terminal]})

        for i in range(len(expression)):
            first_char = expression[i][0]
            #print(first_char)

            
            if first_char in non_terminals:
                for elem in grammar_first[first_char]:
                    #print("elem = %s" % elem)
                    #print("non_terminal = %s" % non_terminal)
                    '''for i in expression:
                        print(i)
                        if first_char not in i:
                            print("Alou")'''
                    indexT = terminals.index(elem)
                    indexNT = non_terminals.index(non_terminal)
                    
                    parse_table[indexNT][indexT] = {non_terminal: grammar[non_terminal]}
            
            if first_char in terminals:   
                aux = ""
                #Verifica se tem &
                '''for x in grammar2[non_terminal]:
                    if '&' in x:
                        grammar2[non_terminal].remove(['&'])'''

                indexT = terminals.index(first_char)
                indexNT = non_terminals.index(non_terminal)
                
                parse_table[indexNT][indexT] = {non_terminal: grammar[non_terminal]}

            if first_char == OP.EPSILON:
                for elem in grammar_follow[non_terminal]:
                    indexT = terminals.index(elem)
                    indexNT = non_terminals.index(non_terminal)
                    parse_table[indexNT][indexT] = {non_terminal: OP.EPSILON}
    
    for i in range(len(non_terminals)):
        print(parse_table[i])
    
    #print(parse_table)
    return(parse_table)

def display_parse_table(parse_table, terminal, non_terminal):
    print("\t\t\t\t",end = "")
    for terminal in terminals:
        print(terminal+"\t\t", end = "")
    print("\n\n")
    
    for non_terminal in non_terminals:
        print("\t\t"+non_terminal+"\t\t", end = "")
        for terminal in terminals:
            print(parse_table[non_terminals.index(non_terminal)][terminals.index(terminal)]+"\t\t", end = "")
        print("\n")

#parsing_table(sentencas, first_list, follow_list, terminais)


table = generate_parse_table(terminals, non_terminals,sentencas, first_list, follow_list)
#print(removeEpsilon(sentencas,"E"))

#display_parse_table(table,terminals,non_terminals)
