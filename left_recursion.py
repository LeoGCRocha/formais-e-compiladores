# Assert
# Grammar without e-production and without circular productions
def fileToDic(file):
    f = open(file)
    mapOfProductions = {}
    for line in f:
        line = line.replace('\n','')  
        production = line.split('->') 
        production[0] = production[0].strip()
        mapOfProductions[production[0]] = production[1].strip()
    return mapOfProductions
production = fileToDic("inputs/left.txt")
# Prepare to remove indirect
def removeEpsilonAndPrepare(productions):
    prod = productions.copy()
    for key in prod:
        if '|' in prod[key]:
            split_array = prod[key].split('|')
            # Remove epsilon
            if '&' in split_array:
                split_array.remove('&')
            prod[key] = [x.strip() for x in split_array]
    return prod
withoutEpsilon = removeEpsilonAndPrepare(production)
def eliminateIndirectRecursion(productions):
    i = 0
    j = 0
    for key, value in productions.items():
        # Remove indirect recursion
        for keyDic, valueDic in productions.items():
            if j > i:
                # Iterate in all sentences
                for sentence in valueDic:
                    # If the first symbol is the same as the key, then replace the first symbol
                    if sentence[0] == key:
                        # Replace if all possibilites
                        values = []
                        for valueToAdd in value:
                            values.append(valueToAdd + sentence[1:])
                        productions[keyDic] = values
            j = j + 1
        j = 0
        i = i + 1
    return productions
withoutIndirect = eliminateIndirectRecursion(withoutEpsilon)
print(withoutIndirect)
def eliminateDirectRecursion(productions):
    dic_without_recursion = {}
    for key, value in productions.items():
        isLeftRecursive = False
        for sentence in value:
            if sentence[0] == key:
                isLeftRecursive = True
        # No resursives, just copy the sentence
        if not isLeftRecursive:
            dic_without_recursion[key] = value
        else:
            # Is left recursive, remove the first symbol
            pass
    return dic_without_recursion
withoutDirect = eliminateDirectRecursion(withoutIndirect)
print(withoutDirect)