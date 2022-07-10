def LeftFactoring(productions):
    # Example   
    # S-> ad|ac|b
    newDict = {}
    # Ireterate in all productions
    for key in productions:
        prods = productions[key]
        # prods : [ad, ac, b]
        temp = dict()
        # Array with the transitions to each symbol
        # a -> [ad, ac] && b -> [b]
        for subprod in prods:
            if subprod[0] not in list(temp.keys()):
                temp[subprod[0]] = [subprod]
            else:
                temp[subprod[0]].append(subprod)
        print(temp)
        # if value list count for any key in temp is > 1,
        # - it has left factoring
        # new_rule stores new subrules for current LHS symbol
        new_rule = []
        # temp_dict stores new subrules for left factoring
        tempo_dict = {}
        for term_key in temp:
            # get value from temp for term_key
            allStartingWithTermKey = temp[term_key]
            if len(allStartingWithTermKey) > 1:
                # left factoring required
                # to generate new unique symbol
                # - add ' till unique not generated
                lhs_ = key + "'"
                while (lhs_ in productions.keys()) \
                        or (lhs_ in tempo_dict.keys()):
                    lhs_ += "'"
                # append the left factored result
                new_rule.append([term_key, lhs_])
                # add expanded rules to tempo_dict
                ex_rules = []
                for g in temp[term_key]:
                    ex_rules.append(g[1:])
                tempo_dict[lhs_] = ex_rules
            else:
                # no left factoring required
                new_rule.append(allStartingWithTermKey[0])
        # add original rule
        newDict[key] = new_rule
        # add newly generated rules after left factoring
        for key in tempo_dict:
            newDict[key] = tempo_dict[key]
    return newDict
# S -> Aa | Sb
# A -> Sc | d
rules= {"S": ["Aa", "Sb"], "A": ["Sc", "d"]}
result= LeftFactoring(rules)
for y in result:    
    print(y, "->", result[y])