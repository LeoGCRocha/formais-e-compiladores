# pass rule in first function
def first(rule):
    global rules, nonterm_userdef, \
        term_userdef, diction, firsts
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
                indivRes = first(itr)
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
                    ansNew = first(rule[1:])
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
def follow(nt):
    global start_symbol, rules, nonterm_userdef, \
        term_userdef, diction, firsts, follows
    # for start symbol return $ (recursion base case)
 
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
                        res = first(subrule)
                        # if epsilon in result apply rule
                        # - (A->aBX)- follow of -
                        # - follow(B)=(first(X)-{ep}) U follow(A)
                        if '&' in res:
                            newList = []
                            res.remove('&')
                            ansNew = follow(curNT)
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
                            res = follow(curNT)
 
                    # add follow result in set form
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)
 
 
def computeAllFirsts():
    global rules, nonterm_userdef, \
        term_userdef, diction, firsts
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
 
    print(f"\nRules: \n")
    for y in diction:
        print(f"{y}->{diction[y]}")
    # print(f"\nAfter elimination of left recursion:\n")
 
    # diction = removeLeftRecursion(diction)
    # for y in diction:
    #     print(f"{y}->{diction[y]}")
    # print("\nAfter left factoring:\n")
 
    # diction = LeftFactoring(diction)
    # for y in diction:
    #     print(f"{y}->{diction[y]}")
 
    # calculate first for each rule
    # - (call first() on all RHS)
    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y):
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)
 
        # save result in 'firsts' list
        firsts[y] = t
 
    print("\nFirsts: ")
    key_list = list(firsts.keys())
    index = 0
    print (firsts)
    # for gg in firsts:
    #     print(f"first({key_list[index]}) "
    #           f"=> {firsts.get(gg)}")
    #     index += 1
 
 
def computeAllFollows():
    global start_symbol, rules, nonterm_userdef,\
        term_userdef, diction, firsts, follows
    for NT in diction:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset
 
    print("\nFollows: ")
    print(follows)
    # key_list = list(follows.keys())
    # index = 0
    # for gg in follows:
    #     print(f"follow({key_list[index]})"
    #           f" => {follows[gg]}")
    #     index += 1

rules=["S -> A b | A B c",
       "B -> b B | A d | & ",
       "A -> a A | &"]
nonterm_userdef=['A', 'S', 'B']
term_userdef=['a', 'b', 'c', 'd']

diction = {}
firsts = {}
follows = {}

computeAllFirsts()
start_symbol = list(diction.keys())[0]
computeAllFollows()