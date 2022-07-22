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
                last_value = stack.pop()
                last_token = tokens[-1]
                # Verificar se /
                # Verificar se eh & 
                # if table[last_token] == "-":
                #     return False
                # elif table[last_token] == "&":
                #     pass
                # else:
                #     next_to_add = table[last_token]
                #     break
                print(last_value)
                print(last_token)
        break
tokens = readTokensAndPrepare("outputs/tokens.txt")
print(tokens)
validateCode("S", tokens, {}, {}, {})