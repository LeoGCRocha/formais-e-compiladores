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
def validateCode(start_symbol, tokens, first, follows, table):
    # Stack buffer
    stack = ["$", start_symbol]
    while True:
        if stack == ["$"] and tokens == ["$"]:
            # Valid code.
            print("Accepted")
            return True
        else:
            if tokens[-1] == stack[-1]:
                tokens.pop()
                stack.pop()
            else:
                last_value = stack[-1].pop()
                last_token = tokens[-1]
                # Verificar se /
                # Verificar se eh & 
                if table[last_token] == "-":
                    print("Syntatic error")
                    return False
                elif table[last_token] == "&":
                    # Remove from stack without pass to next token
                    pass
                else:
                    next_to_add = table[last_token]
                    # Identificar os simbolos parte a parte
                    break
tokens = readTokensAndPrepare("outputs/tokens.txt")
print(tokens)
validateCode("S", tokens, {}, {}, {})