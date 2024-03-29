from copy import deepcopy
from operators import Operators as OP
import csv
import utils

#sentencas = {"E":["TE'"],"E'":["+TE'","&"],"T":["FT'"],"T'":["*FT'","&"],"F":["id","(E)"]}
#sentencas_trat = {'E': [['T', "E'"]], "E'": [['+', "T", "E'"],['&']], "T": [['F', "T'"]],"T'": [['*', "F", "T'"],['&']],"F": [['id'],['(', "E", ")"]]}

#first_list = {'E': {'(','id'}, "E'": {'+','&'}, "T": {'(', 'id'}, "T'": {'*',"&"}, "F": {'(', 'id'}}
#follow_list = {'E': {'$',')'}, "E'": {'$',')'}, "T": {'+', '$',')'}, "T'": {'+', '$',')'}, "F": {'*', '+','$', ')'}}
#terminals = ['id', '+', '*', '(', ')', '$']
#non_terminals = ['E',"E'","T","T'","F"]

# sentencas_trat = {'E': [['T'],["E'"]], "E'": [['+', "T", "E'"], ['&']], "T": [['F', "T'"]], "T'": [['*', "F", "T'"], ['&']], "F": [['¬', "F"], ['id']]}
# sentencas_trat2 = {'E': [['T',"E'"]], "E'": [['+', "T", "E'"], ['&']], "T": [['F', "T'"]], "T'": [['*', "F", "T'"], ['&']], "F": [['¬', "F"], ['id']]}
# sentencas = {"E":["TE'"],"E'":["+TE'","&"],"T":["FT'"],"T'":["*FT'","&"],"F":["¬F","id"]}
# first_list = {'E': {'¬','id'}, "E'": {'&','+'}, "T": {'¬', 'id'}, "T'": {'*',"&"}, "F": {'¬', 'id'}}
# follow_list = {'E': {'$'}, "E'": {'$'}, "T": {'$', '+'}, "T'": {'$', '+'}, "F": {'*', '$', '+'}}
# terminals = ['id', '+', '*', '¬', '$']
# non_terminals = ['E',"E'","T","T'","F"]

#sentencas = {'S': [['A', 'k', 'O']], 'A': [['a', "A''"]], "A''": [['B', "A'"], ['C', "A'"]], 'C': [['c']], 'B': [['b', 'B', 'C'], ['r']], "A'": [['d', "A'"], ['&']]}
#first_list = {'S': {'a'}, 'A': {'a'}, "A''": {'r', 'b', 'c'},'C': {'c'}, 'B': {'r', 'b'}, "A'": {'&', 'd'}}
#follow_list = {'S': {'$'}, 'A': {'k'}, "A''": {'k'}, 'C': {'k', 'd', 'c'}, 'B': {'k', 'd', 'c'}, "A'": {'k'}}
#terminals = ['k', 'O', 'd', 'a', 'c', 'b', 'r','$']
#non_terminals = ["S", "A", "A''", "C", "B", "A'"]

# sentencas_trat = {'P': [['K', "L"],['b','K','L','e']], "K": [['c', "K"], ['T','V']], "T": [['t', "T'"],['&']], "V": [['v', "V'"]],"V'": [['V'],["&"]], "L": [['J']], "J": [['a',"J'"],["e","J'"]], "J'": [['c',"J'"],["&"]]}
# first_list = {'P': {'c','b','t','v','&'}, "K": {'c','t','v','&'}, "T": {'t', '&'}, "V": {'v'}, "V'": {'v', '&'}, "L": {'a', 'e'}, "J": {'a', 'e'}, "J'": {'c', '&'}}
# follow_list = {'P': {'$'}, "K": {'a','e'}, "T": {'v'}, "V": {'a','e'}, "V'": {'a','e'}, "L": {'e', '$'}, "J": {'e', '$'}, "J'": {'e', '$'}}
# terminals = ['e', 'c', 't', 'v', 'a', 'b','$']
# non_terminals = ['P',"K","T","V","V'","L","J","J'"]

def adapt_grammar(grammar, terminals):
    # {"E":["TE'"],"E'":["+TE'","&"],"T":["FT'"],"T'":["*FT'","&"],"F":["id","(E)"]}
    new_grammar = {}
    for key,value in grammar.items():
        new_grammar[key] = []
    for key, value in grammar.items():
        value_to_add = []
        for item in value:
            value_to_add.append(item.split())
        new_grammar[key] = value_to_add
    return new_grammar

def adapt_symbol(grammar):
    for non_terminal, expression in grammar.items():
        print(expression)

def generate_parse_table(terminals, non_terminals, grammar, grammar_first, grammar_follow):
    parse_table = [["-"]*len(terminals) for i in range(len(non_terminals))]
    grammar2 = deepcopy(grammar)

#Percorre os a gramática que se baseia em um dicionario {"Nao terminal": [Expressao, Expressao2 ...]}

    for non_terminal, expression in grammar.items():
        
        # Pegamos a primeiro char de cada subexpressao para determinar a regra
        # Ex: A -> BC | dE | &
        # 1 Iteração) First_char = B
        # 2 Iteração) First_char = d
        # 3 Iteração) First_char = &
        # Entrando em suas regras
        # Após isso pulamos para próxima expressao 

        for i in range(len(expression)):
            first_char = expression[i][0]
            #print("Expression = %s"%expression)
            #print("First Char = %s"%first_char)
            
            # Se o primeiro char é um não terminal
            
            if first_char in non_terminals:
                
                #Percorremos o first[NT2] da sentenca NT -> NT2 B | NT3
                # Ex: A -> BC | DE
                # Pegamos first[B] e para todo ParseTable[A][First de B] adicionamos a expressao A -> BC
                # Na outra iteração pegamos first[D] e para todo ParseTable[A][First de D] adicionamos a expressao A -> DE
                for elem in grammar_first[first_char]:           
                    # Criamos uma grammar2 apenas como variavel aux
                    grammar2 = deepcopy(grammar)
                    for j in grammar[non_terminal]:
                        if j[0] == first_char and elem != "&":
                            lista = list(filter(j.__eq__, grammar[non_terminal]))
                            
                            grammar2[non_terminal] = lista
                            
                            indexT = terminals.index(elem)
                            indexNT = non_terminals.index(non_terminal)
                            
                            parse_table[indexNT][indexT] = {non_terminal: grammar2[non_terminal]}
                            
                            grammar2 = deepcopy(grammar)
                        #Caso que tem & no first do first_char
                        # Adicionamos nos follows do Non terminal
                        if j[0] == first_char and elem == "&":
                            lista = list(filter(j.__eq__, grammar[non_terminal]))
                            grammar2[non_terminal] = lista

                            for j in grammar_follow[non_terminal]:
                                indexT = terminals.index(j)
                                indexNT = non_terminals.index(non_terminal)
                                parse_table[indexNT][indexT] = {non_terminal: grammar2[non_terminal]}
                            
                            grammar2 = deepcopy(grammar)
            
            # Se o primeiro char é um terminal

            if first_char in terminals:   
                # Criamos uma grammar2 apenas como variavel aux
                grammar2 = deepcopy(grammar)

                for k in grammar[non_terminal]:
                    if k[0] == first_char: 
                        lista = list(filter(k.__eq__, grammar[non_terminal]))
                        grammar2[non_terminal] = lista
                        
                        #Percorremos a expressão NT -> T NT
                        # Ex: A -> aBC | id
                        # Adicionamos ParseTable[A][a] adicionamos a expressao A -> aBC
                        # Na outra iteração adicionamos ParseTable[A][id] adicionamos a expressao A -> id

                        indexT = terminals.index(first_char)
                        indexNT = non_terminals.index(non_terminal)
                        
                        parse_table[indexNT][indexT] = {non_terminal: grammar2[non_terminal]}
                        grammar2 = deepcopy(grammar)
            
            # Se o primeiro char é um &
            if first_char == OP.EPSILON:
                #Percorremos a expressão NT -> NT | &
                # Na iteração que o first_char = &
                # Ex: A -> Bc | &
                # Pegamos Follow[A] e para todo ParseTable[A][Follow de A] adicionamos a expressao A -> &

                for elem in grammar_follow[non_terminal]:
                    indexT = terminals.index(elem)
                    indexNT = non_terminals.index(non_terminal)
                    parse_table[indexNT][indexT] = {non_terminal: OP.EPSILON}
    return(parse_table)

def parseToCsv(table, non_terminals, terminals, file):
    header = [" "]
    for symbol in terminals:
        header.append(symbol)
    # parseToCsv
    with open(file, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(len(non_terminals)):
            row = [non_terminals[i]]
            for element in table[i]:
                row.append(element)
            writer.writerow(row)
    utils.csv_to_table("outputs/parse_table.csv", "outputs/csv_files/parse_table.csv")

#table = generate_parse_table(terminals, non_terminals,sentencas_trat, first_list, follow_list)
#table = generate_parse_table(terminals, non_terminals,adapt_grammar(sentencas), first_list, follow_list)
