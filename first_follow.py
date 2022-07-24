def first(rule, start_symbol, rules, nonterm_userdef, term_userdef, dic, firsts, follows):
    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '&':
            return '&'
    if len(rule) != 0:
        if rule[0] in list(dic.keys()):
            fres = []
            rhs_rules = dic[rule[0]]
            for itr in rhs_rules:
                indivRes = first(itr, start_symbol, rules, nonterm_userdef, term_userdef, dic, firsts, follows) 
                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                else:
                    fres.append(indivRes)

            if '&' not in fres:
                return fres
            else:
                newList = []
                fres.remove('&')
                if len(rule) > 1:
                    ansNew = first(rule[1:], start_symbol, rules, nonterm_userdef, term_userdef, dic, firsts, follows)
                    if ansNew != None:
                        if type(ansNew) is list:
                            newList = fres + ansNew
                        else:
                            newList = fres + [ansNew]
                    else:
                        newList = fres
                    return newList
                fres.append('&')
                return fres

def follow(nt, start_symbol, rules, nonterm_userdef, term_userdef, dic, firsts, follows):
    solset = set()
    if nt == start_symbol:
        solset.add('$')
    for curNT in dic:
        rhs = dic[curNT]
        for subrule in rhs:
            if nt in subrule:
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]
                    if len(subrule) != 0:
                        res = first(subrule, start_symbol, rules, nonterm_userdef, term_userdef, dic, firsts, follows)
                        if '&' in res:
                            newList = []
                            res.remove('&')
                            ansNew = follow(curNT, start_symbol, rules, nonterm_userdef, term_userdef, dic, firsts, follows)
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:
                        if nt != curNT:
                            res = follow(curNT, start_symbol, rules, nonterm_userdef, term_userdef, dic, firsts, follows)
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)
def computeFirsts(start_symbol, rules, nonterm_userdef, term_userdef, dic, firsts, follows):
    for rule in rules:
        k = rule.split("->")
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        dic[k[0]] = multirhs 
    for y in list(dic.keys()):
        t = set()
        for sub in dic.get(y):
            res = first(sub, start_symbol, rules, nonterm_userdef, term_userdef, dic, firsts, follows)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)
        firsts[y] = t

def computeFollows(start_symbol, rules, nonterm_userdef, term_userdef, dic, firsts, follows):
    for NT in dic:
        solset = set()
        sol = follow(NT, start_symbol, rules, nonterm_userdef, term_userdef, dic, firsts, follows)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset

def filetoDic(file, rules):
    f = open(file, 'r')
    for line in f:
        rules.append(line.rstrip())

def searchNonTerm(nonterm_userdef, productions):
    for key in productions.keys():
        nonterm_userdef.append(key)

def searchTerm(term_userdef, rules, productions):
    for rule in rules:
        rule = rule.split("->")
        term =  list(map(str.strip, rule[1].split("|")))
        for x in term:
            for y in x.split():
                if y not in term_userdef and y not in productions.keys():
                    term_userdef.append(y)
    
def generateFirstAndFollow(file, productions):
    rules = []
    nonterm_userdef = []
    term_userdef = []
    # Prepare Gramar
    filetoDic(file, rules)
    searchNonTerm(nonterm_userdef, productions)
    searchTerm(term_userdef, rules, productions)
    # Generate Firsts
    dic = {}
    firsts = {}
    follows = {}
    computeFirsts(rules[0][0], rules, nonterm_userdef, term_userdef, dic, firsts, follows)
    start_symbol = list(dic.keys())[0]
    computeFollows(start_symbol, rules, nonterm_userdef, term_userdef, dic, firsts, follows)
    return [firsts, follows, nonterm_userdef, term_userdef]