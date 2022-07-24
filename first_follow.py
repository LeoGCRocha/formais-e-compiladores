# pass rule in first function
def first(rule, start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows):
    # condição base de recursão
    # (para terminal ou epsilon)
    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '&':
            return '&'
    # Condição para não-terminais
    if len(rule) != 0:
        if rule[0] in list(diction.keys()):
            # fres -> Lista temporária de resultados
            fres = []
            rhs_rules = diction[rule[0]]
            for itr in rhs_rules:
                indivRes = first(itr, start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows) 
                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                else:
                    fres.append(indivRes)

            if '&' not in fres:
                return fres
            else:
                # apply epsilon
                # rule => f(ABC)=f(A)-{e} U f(BC)
                newList = []
                fres.remove('&')
                if len(rule) > 1:
                    ansNew = first(rule[1:], start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows)
                    if ansNew != None:
                        if type(ansNew) is list:
                            newList = fres + ansNew
                        else:
                            newList = fres + [ansNew]
                    else:
                        newList = fres
                    return newList
                # if result is not already returned
                # - control reaches here
                # lastly if eplison still persists
                # - keep it in result of first
                fres.append('&')
                return fres

# calculation of follow
# use 'rules' list, and 'diction' dict from above
# follow function input is the split result on
# - Non-Terminal whose Follow we want to compute
def follow(nt, start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows):
    solset = set()
    if nt == start_symbol:
        # return '$'
        solset.add('$')
    # check all occurrences
    # solset - is result of computed 'follow' so far
    # For input, check in all rules
    for curNT in diction:
        rhs = diction[curNT]
        # go for all productions of NT
        for subrule in rhs:
            if nt in subrule:
                # call for all occurrences on
                # - non-terminal in subrule
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]
                    # empty condition - call follow on LHS
                    if len(subrule) != 0:
                        # compute first if symbols on
                        # - RHS of target Non-Terminal exists
                        res = first(subrule, start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows)
                        # if epsilon in result apply rule
                        # - (A->aBX)- follow of -
                        # - follow(B)=(first(X)-{ep}) U follow(A)
                        if '&' in res:
                            newList = []
                            res.remove('&')
                            ansNew = follow(curNT, start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows)
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:
                        # when nothing in RHS, go circular
                        # - and take follow of LHS
                        # only if (NT in LHS)!=curNT
                        if nt != curNT:
                            res = follow(curNT, start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows)
                    # add follow result in set form
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)
def computeAllFirsts(start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows):
    for rule in rules:
        k = rule.split("->")
        # remove un-necessary spaces
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        # remove un-necessary spaces
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs 
    # calculate first for each rule
    # - (call first() on all RHS)
    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y):
            res = first(sub, start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)
        # save result in 'firsts' list
        firsts[y] = t

def computeAllFollows(start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows):
    for NT in diction:
        solset = set()
        sol = follow(NT, start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows)
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

def removeRepeated(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l
    
def generateFirstAndFollow(file, productions):
    rules = []
    nonterm_userdef = []
    term_userdef = []
    # Prepare Gramar
    filetoDic(file, rules)
    searchNonTerm(nonterm_userdef, productions)
    searchTerm(term_userdef, rules, productions)
    # Generate Firsts
    diction = {}
    firsts = {}
    follows = {}
    computeAllFirsts(rules[0][0], rules, nonterm_userdef, term_userdef, diction, firsts, follows)
    start_symbol = list(diction.keys())[0]
    computeAllFollows(start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows)
    return [firsts, follows, nonterm_userdef, term_userdef]