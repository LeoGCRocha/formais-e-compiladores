# Assert
# Grammar without e-production and without circular productions
from collections import OrderedDict
def fileToDic(file):
    f = open(file)
    mapOfProductions = OrderedDict()
    for line in f:
        line = line.replace('\n','')  
        production = line.split('->') 
        production[0] = production[0].strip()
        mapOfProductions[production[0]] = production[1].strip()
    return mapOfProductions
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
        else:
            prod[key] = [prod[key]]
    return prod
# Eliminate indirect recursion
def eliminateIndirectRecursion(productions):
    i = 0
    j = 0
    for key, value in productions.items():
        # Remove indirect recursion
        for keyDic, valueDic in productions.items():
            if j > i:
                # Iterate in all sentences
                for sentence in valueDic:
                    if sentence[0] == key:
                        backup = productions[keyDic]
                        posToAdd = backup.index(sentence)
                        backup.remove(sentence)
                        posFixKey = sentence[1:]
                        # Add new values
                        toAdd = [x+posFixKey for x in value]
                        for x in toAdd:
                            backup.insert(posToAdd, x)
                        productions[keyDic] = backup
                    break
            j = j + 1
        j = 0
        i = i + 1
    return productions
# Eliminate Direct Recursion
def eliminateDirectRecursion(productions):
    dic_without_recursion = OrderedDict()
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
            while newKeyValue in dic_without_recursion:
                newKeyValue = newKeyValue + "'"
            resursive_values = []
            not_recursive_values = []
            for sentence in value:
                if sentence[0] == key:
                    # A -> Aa 
                    resursive_values.append(sentence[1:] + " "+newKeyValue)
                else:
                    # E -> ab | EC
                    # E -> abE'
                    not_recursive_values.append(sentence + " "+newKeyValue)
            resursive_values.append("&")
            dic_without_recursion[key] = not_recursive_values
            dic_without_recursion[newKeyValue] = resursive_values
    return dic_without_recursion
# fixFirstProd
def fixFirstProd(productions):
    first_value = list(productions)[-1]
    isLeftRecursive = False
    for sentence in productions[first_value]:
        if sentence[0] == first_value:
            isLeftRecursive = True
            break
    if isLeftRecursive:
        new_dic = productions.copy()
        # Is left recursive, remove the first symbol
        newKeyValue = first_value + "'"
        while newKeyValue in new_dic:
            newKeyValue = newKeyValue + "'"
        resursive_values = []
        not_recursive_values = []
        for sentence in productions[first_value]:
            if sentence[0] == first_value:
                # A -> Aa 
                resursive_values.append(sentence[1:] + " " +newKeyValue)
            else:
                # E -> ab | EC
                # E -> abE'
                not_recursive_values.append(sentence + " " + newKeyValue)
        resursive_values.append("&")
        new_dic[first_value] = not_recursive_values
        new_dic[newKeyValue] = resursive_values
        return new_dic
    else:
        return productions
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
# Method
def eliminateLeftRecursion(file):
    productions = fileToDic(file)
    withouEpsilon = removeEpsilonAndPrepare(productions)
    withoutFirst = fixFirstProd(withouEpsilon)
    withoutIndirect = eliminateIndirectRecursion(withouEpsilon)
    withoutDirect = eliminateDirectRecursion(withoutIndirect)
    leftRecursive = True
    while leftRecursive:
        leftRecursive = False
        for key, value in withoutDirect.items():
            for val in value:
                if key == val[0]:
                    leftRecursive = True
                    break
        if leftRecursive:
            withoutFirst = fixFirstProd(withoutDirect)
            withoutIndirect = eliminateIndirectRecursion(withoutFirst)
            withoutDirect = eliminateDirectRecursion(withoutIndirect)
        else:
            # Fix Production 
            new_dic = {}
            for key, value in withoutDirect.items():
                value_to_add = []
                for val in value:
                    value_to_add.append(val.strip())
                new_dic[key] = value_to_add
            return new_dic