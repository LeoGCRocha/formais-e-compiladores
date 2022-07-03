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
                values = []
                # Iterate in all sentences
                for sentence in valueDic:
                    # If the first symbol is the same as the key, then replace the first symbol
                    if sentence[0] == key:
                        # Replace if all possibilites
                        # TODO: Fix this
                        pass
                    # else:
                    #     values.append(sentence)
                productions[keyDic] = values
            j = j + 1
        j = 0
        i = i + 1
    return productions
withoutIndirect = eliminateIndirectRecursion(withoutEpsilon)
print(withoutIndirect)
# Eliminate Direct Recursion
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
            newKeyValue = key + "'"
            resursive_values = []
            not_recursive_values = []
            for sentence in value:
                if sentence[0] == key:
                    # A -> Aa 
                    resursive_values.append(sentence[1:] + newKeyValue)
                else:
                    # E -> ab | EC
                    # E -> abE'
                    not_recursive_values.append(sentence + newKeyValue)
            resursive_values.append("&")
            dic_without_recursion[key] = not_recursive_values
            dic_without_recursion[newKeyValue] = resursive_values
    return dic_without_recursion
# Output dictionary
def dicToFile(dic, file):
    f = open(file, 'w')
    for key, value in dic.items():
        f.write(key + " -> ")
        stringToWrite = ""
        for sentence in value:
            stringToWrite = stringToWrite + sentence + " | "
        stringToWrite = stringToWrite[:-3]
        f.write(stringToWrite + "\n")
    f.close()
withoutDirect = eliminateDirectRecursion(withoutIndirect)
dicToFile(withoutDirect, "outputs/left.txt")