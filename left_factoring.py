from operators import Operators as OP
from files import Files
from utils import *

def left_factoring(language):
    # replace empty productions to epsilon
    for key, value in language.items():
        language[key] = list(map(lambda x: x if x != "" else OP.EPSILON, value))

    # one time factored language
    new_language = {}
    
    # iterate through all symbols (keys) and productions
    for key, productions in language.items():
        # productions: [['a', 'S'], 'b', ...]

        # symbol -> production
        # links a symbol s to each production which initial symbol is s
        subproductions = dict()

        # builds subproductions 
        for subproduction in productions:
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

                # append the left factored result
                # now after term_key comes the new production
                new_rule.append([term_key, new_rule_symbol])

                # fixes old productions to fit in new production
                ex_rules = []
                for g in same_key:
                    ex_rules.append(g[1:])
                new_subrules[new_rule_symbol] = ex_rules
            else:
                # no left factoring required
                new_rule.append(same_key[0])

        # sets current symbol rule
        new_language[key] = new_rule

        # add newly generated rules after left factoring
        for key in new_subrules:
            new_language[key] = new_subrules[key]

    # call left_factoring until no more changes are detected
    if (language != new_language):
        return left_factoring(new_language)

    return new_language

def test():
    # language = {
    #     "S": ["acd", "ac"], 
    #     "A": ["bd", "bdef"],
    # }
    # language = {"S": ["c", "a", "b"]}
    language = language_read(Files.IN_LEFT_FACTORING1)
    result = left_factoring(language)
    language_write(Files.OUT_LEFT_FACTORING1, result)
    # result= left_factoring(language)
    # for y in result:    
    #     print(y, "->", result[y])

if __name__ == "__main__":
    test()