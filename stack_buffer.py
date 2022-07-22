import parsingtable as pt
from copy import deepcopy
def readTokensAndPrepare(file):
    tokens = ["$"]
    with open(file, "r") as f:
        tokens2 = []
        for line in f:
            # Remove , 
            tokens2.append(line.split(" ")[1][:-1])
        tokens2.reverse()
        tokens.extend(tokens2)
    return tokens
def validateCode(start_symbol, tokens, non_terminals, terminals, table):
    # Stack buffer
    stack = ["$", start_symbol]
    contador = 0
    while True:
        if stack == ["$"] and tokens == ["$"]:
            # Valid code.
            return True
        else:
            if tokens[-1] == stack[-1]:
                tokens.pop()
                stack.pop()
            else:
                last_value = stack.pop()
                last_token = tokens[-1]
                # Nonterminal table
                index1 = non_terminals.index(last_value)
                # Terminal table
                index2 = terminals.index(last_token)
                production = table[index1][index2]
                if production == "-":
                    return False
                else:
                    production = deepcopy(production[last_value])
                    if production == "&":
                        pass
                    else: 
                        production = deepcopy(production[0])
                        production.reverse()
                        stack.extend(production)
# tokens = readTokensAndPrepare("outputs/tokens2.txt")
# sentencas_trat = {'E': [['T',"E'"]], "E'": [['+', "T", "E'"], ['&']], "T": [['F', "T'"]], "T'": [['*', "F", "T'"], ['&']], "F": [['¬', "F"], ['id']]}
# sentencas = {"E":["TE'"],"E'":["+TE'","&"],"T":["FT'"],"T'":["*FT'","&"],"F":["¬F","id"]}
# first_list = {'E': {'¬','id'}, "E'": {'&','+'}, "T": {'¬', 'id'}, "T'": {'*',"&"}, "F": {'¬', 'id'}}
# follow_list = {'E': {'$'}, "E'": {'$'}, "T": {'$', '+'}, "T'": {'$', '+'}, "F": {'*', '$', '+'}}
# terminals = ['id', '+', '*', '¬', '$']
# non_terminals = ['E',"E'","T","T'","F"]
# table = pt.generate_parse_table(terminals, non_terminals, sentencas_trat, first_list, follow_list)
# pt.parseToCsv(table, non_terminals, terminals, "outputs/parse_table.csv")
# validateCode("E", tokens, non_terminals, terminals, table)