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
                try:
                    # Nonterminal table
                    index1 = non_terminals.index(last_value)
                    # Terminal table
                    index2 = terminals.index(last_token)
                except ValueError:
                    return False
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