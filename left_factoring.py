import copy
from functools import reduce
from operators import Operators as OP
from files import Files
from utils import *


def remove_indirects(indirect_language, multiple_symbols_identifiers):
    language = copy.deepcopy(indirect_language)

    for key, value in language.items():
        language[key] = list(map(lambda x: x if x != "" else OP.EPSILON, value))
    
    # sorts msi list from bigger words to smaller words
    multiple_symbols_identifiers.sort(
        key = lambda msi : len(msi), reverse = True
    )

    for key, productions in language.items():
        # productions: [['a', 'S'], 'b', ...]

        # symbol -> production
        # links a symbol s to each production which initial symbol is s
        subproductions = dict()

        # builds subproductions 
        for subproduction in productions:
            starts_with_msi = False
            for msi in multiple_symbols_identifiers:
                if subproduction.startswith(msi):
                    starts_with_msi = True
                    break

            if (starts_with_msi):
                if msi not in list(subproductions.keys()):
                    subproductions[msi] = [subproduction]
                else:
                    subproductions[msi].append(subproduction)
            else:
                if subproduction[0] not in list(subproductions.keys()):
                    subproductions[subproduction[0]] = [subproduction]
                else:
                    subproductions[subproduction[0]].append(subproduction)
        
        new_productions = []
        for k, v in subproductions.items():
            if k in language.keys():
                for x in v:
                    language[key].remove(x)
                    for y in language[k]:
                        new_productions.append(x.replace(k,y))
                language[key].extend(new_productions)
                return language
        
    return language
                

def do_left_factoring(language, multiple_symbols_identifiers):
    # replace empty productions to epsilon
    for key, value in language.items():
        language[key] = list(map(lambda x: x if x != "" else OP.EPSILON, value))
    
    # sorts msi list from bigger words to smaller words
    multiple_symbols_identifiers.sort(
        key = lambda msi : len(msi), reverse = True
    )

    # one time factored language
    new_language = {}

    # stores new rule symbols
    new_symbols = []

    # iterate through all symbols (keys) and productions
    for key, productions in language.items():
        # productions: [['a', 'S'], 'b', ...]

        # symbol -> production
        # links a symbol s to each production which initial symbol is s
        subproductions = dict()

        # builds subproductions 
        for subproduction in productions:
            starts_with_msi = False
            for msi in multiple_symbols_identifiers:
                if subproduction.startswith(msi):
                    starts_with_msi = True
                    break

            if (starts_with_msi):
                if msi not in list(subproductions.keys()):
                    subproductions[msi] = [subproduction]
                else:
                    subproductions[msi].append(subproduction)
            else:
                if subproduction[0] not in list(subproductions.keys()):
                    subproductions[subproduction[0]] = [subproduction]
                else:
                    subproductions[subproduction[0]].append(subproduction)
        # stores new productions of currrent key
        new_rule = []

        # stores new subrules for left factoring
        new_subrules = {}

        for term_key, same_key in subproductions.items():
            # if same_key length > 1, factoring is required
            if len(same_key) > 1:
                new_rule_symbol = key + "'"

                # ensures new_rule_symbol is an unique symbol
                while (new_rule_symbol in language.keys()) \
                    or (new_rule_symbol in new_subrules.keys()):
                    new_rule_symbol += "'"

                new_symbols.append(new_rule_symbol)

                # append the left factored result
                # now after term_key comes the new production
                new_rule.append([term_key, new_rule_symbol])

                # fixes old productions to fit in new production
                ex_rules = []
                for g in same_key:
                    ex_rules.append(g[len(term_key):])
                new_subrules[new_rule_symbol] = ex_rules
            else:
                # no left factoring required
                new_rule.append(same_key[0])

        # sets current symbol rule
        new_language[key] = new_rule

        # add newly generated rules after left factoring
        for key in new_subrules:
            new_language[key] = new_subrules[key]
    
    # fixes new_language values format
    # from S -> [[a, b], c]
    # to S -> [ab, c]
    new_language = {
        key : list(map(
            lambda x : "".join(x), new_language[key]
        )) for key in new_language.keys()
    }

    # call left_factoring until no more changes are detected
    multiple_symbols_identifiers = multiple_symbols_identifiers + new_symbols
    if (language != new_language):
        return do_left_factoring(new_language, multiple_symbols_identifiers)

    if (language != new_language):
        return do_left_factoring(new_language, multiple_symbols_identifiers)
    
    language_indirect = remove_indirects(language, multiple_symbols_identifiers)

    if (language != language_indirect):
        return do_left_factoring(language_indirect, multiple_symbols_identifiers)
    return new_language

def left_factoring(language):
    msi = list(set(filter(lambda x : len(x) > 1, 
        reduce(
            list.__add__, [
                x.split() for value in language.values() for x in value
            ]
        ) + list(language.keys())
    )))
    language  = {
        key : list(map(lambda x : "".join(x.split()), language[key]))
        for key in language.keys()
    }
    return do_left_factoring(language, msi)


def test():
    # language = {
    #     "S": ["acd", "ac"], 
    #     "A": ["bd", "bdef"],
    # }
    # language = {"S": ["c", "a", "b"]}
    language, terminals = language_read(Files.IN_LEFT_FACTORING1)
    result = left_factoring(language)
    language_write(Files.OUT_LEFT_FACTORING1, result)
    # result= left_factoring(language)
    # for y in result:
    #     print(y, "->", result[y])

if __name__ == "__main__":
    test()