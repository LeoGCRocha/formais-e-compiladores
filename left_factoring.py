from operators import Operators as OP

def leftFactoring(language):
    for key, value in language.items():
        language[key] = list(map(lambda x: x if x != "" else OP.EPSILON, value))

    # Example
    # S-> ad|ac|b
    newLanguage = {}
    # Ireterate in all productions
    for key, productions in language.items():
        # productions = language[key]
        # productions : [ad, ac, b]
        subproductions = dict()
        # Array with the transitions to each symbol
        # a -> [ad, ac] && b -> [b]
        for subproduction in productions:
            if subproduction[0] not in list(subproductions.keys()):
                subproductions[subproduction[0]] = [subproduction]
            else:
                subproductions[subproduction[0]].append(subproduction)
        # if value list count for any key in subproductions is > 1,
        # - it has left factoring
        # new_rule stores new subrules for current LHS symbol
        newRule = []
        # temp_dict stores new subrules for left factoring
        newSubrules = {}
        for term_key, allStartingWithTermKey in subproductions.items():
            # get value from temp for term_key
            # allStartingWithTermKey = subproductions[term_key]
            if len(allStartingWithTermKey) > 1:
                # left factoring required
                # to generate new unique symbol
                # - add ' till unique not generated
                lhs_ = key + "'"
                while (lhs_ in language.keys()) \
                    or (lhs_ in newSubrules.keys()):
                    lhs_ += "'"
                # append the left factored result
                newRule.append([term_key, lhs_])
                # add expanded rules to newSubrules
                ex_rules = []
                for g in subproductions[term_key]:
                    ex_rules.append(g[1:])
                newSubrules[lhs_] = ex_rules
            else:
                # no left factoring required
                newRule.append(allStartingWithTermKey[0])
        # add original rule
        newLanguage[key] = newRule
        # add newly generated rules after left factoring
        for key in newSubrules:
            newLanguage[key] = newSubrules[key]

    if (language != newLanguage):
        return leftFactoring(newLanguage)

    return newLanguage

rules= {
    "S": ["acd", "ac"], 
    "A": ["bd", "bdef"],
}
# rules= {"S": ["c", "a", "b"]}
result= leftFactoring(rules)
for y in result:    
    print(y, "->", result[y])