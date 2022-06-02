from node import Node
from expression import Expression
from operators import Operators as OP
from automata import *

class SyntaxTree:
    def __init__(self, expression):
        self.__expression = expression
        self.__enumerateCount = 1
        self.__root = Node(OP.CONCAT, self.__build(expression), Node(OP.END))
        self.__dicSymbols = {}
        self.numerateLeaves(self.__root)
        self.setNodes(self.__root)
        self.__followPosTable = []
        self.prepareFollowPos()
        self.setFollowPos(self.__root)
        self.__DFA = None
        self.createAutomata()

    def __build(self, expression):
        first, last, operator = Expression.subExpressions(expression)
        node = Node(operator)
        if (operator == OP.STAR):
            if len(first) == 1:
                node.setLeft(Node(first[0]))
            else:
                node.setLeft(self.__build(first))
        else:
            if (len(first) == 1):
                node.setLeft(Node(first[0]))
            else:
                node.setLeft(self.__build(first))
            if (len(last) == 1):
                node.setRight(Node(last[0]))
            else:
                node.setRight(self.__build(last))
        return node

    def numerateLeaves(self, node):
        if node.isLeaf():
            node.setNum(self.__enumerateCount)
            self.__enumerateCount = self.__enumerateCount + 1
            self.__dicSymbols[node.num()] = node.symbol()
        else:
            if node.left() != None:
                self.numerateLeaves(node.left())
            if node.right() != None:
                self.numerateLeaves(node.right())

    def setNodes(self, node):
        if node != None:
            if node.isLeaf():
                # A leaf labeled &
                if node.symbol() == OP.EPSILON:
                    node.setNullable(True)
                    self.setNodes(node.father())
                else:
                    node.setFirstPos([node.num()])
                    node.setLastPos([node.num()])
                    node.setNullable(False)
                    self.setNodes(node.father())
            else:
                if node.left().nullable() == None:
                    self.setNodes(node.left())
                if node.right().nullable() == None:
                    self.setNodes(node.right())
                if node.symbol() == OP.OR:
                    # An or-node n = c1|c2
                    # node.left c1
                    # node.right c2
                    if node.left().nullable() or node.right().nullable():
                        node.setNullable(True)
                    else: 
                        node.setNullable(False)
                    # firstpos(n) = firstpos(c1) U firstpos(c2)
                    c1c2list = [node.left().firstPos(), node.right().firstPos()]
                    firstpostn = list(set().union(*c1c2list))
                    # lastpos(n) = lastpos(c1) U lastpos(c2)
                    c1c2list = [node.left().lastPos(), node.right().lastPos()]
                    lastpostn = list(set().union(*c1c2list))
                    # set
                    node.setFirstPos(firstpostn)
                    node.setLastPos(lastpostn)
                elif node.symbol() == OP.CONCAT:
                    # A cat-node n = c1c2
                    # node.left c1
                    # node.right c2s
                    if node.left().nullable() and node.right().nullable():
                        node.setNullable(True)
                    else:
                        node.setNullable(False)
                    # nullable(c1)
                    if node.left().nullable():
                        c1c2list = [node.left().firstPos(), node.right().firstPos()]
                        firstpostn = list(set().union(*c1c2list))
                        node.setFirstPos(firstpostn) 
                    else:
                        node.setFirstPos(node.left().firstPos())
                    # nullable(c2) lastpos
                    if node.right().nullable():
                        c2c1list = [node.right().lastPos(), node.left().lastPos()]
                        lastpostn = list(set().union(*c2c1list))
                        node.setLastPos(lastpostn)
                    else:
                        node.setLastPos(node.right().lastPos())
                elif node.symbol() == OP.STAR:
                    # A star-node n = c1*
                    # node c1
                    node.setNullable(True)
                    # firstpos(c1)
                    node.setFirstPos(node.left().firstPos())
                    node.setLastPos(node.left().firstPos())
    def prepareFollowPos(self):
        for _ in range(1, self.__enumerateCount):
            self.__followPosTable.append([])
        self.__followPosTable[-1] = [0]
    def setFollowPos(self, node):
        # from leaves to root
        if not node.isLeaf() and node.symbol() != OP.END:
            self.setFollowPos(node.left())
            self.setFollowPos(node.right())
            if node.symbol() == OP.CONCAT:
                # left node c1
                # right node c2
                # lastpos(c1)  i; each element of firstpos(c2) are in followpos(i)
                c1 = node.left().lastPos()
                c2 = node.right().firstPos()
                for i in c1:
                    listc1c2 = [self.__followPosTable[i-1], c2]
                    self.__followPosTable[i-1] = list(set().union(*listc1c2))
            elif node.symbol() == OP.STAR:
                # i lastpos(n)
                # each element of firstpos(n) are in followpos(i)
                for i in node.lastpos():
                    listc1c2 = [self.__followPosTable[i-1], node.firstpos()]
                    self.__followPosTable[i-1] = list(set().union(*listc1c2))
    def root(self):
        return self.__root
    def DFA(self):
        return self.__DFA
    def followPosTable(self):
        return self.__followPosTable
    def toAutomataLabel(self, list):
        str1 = ','.join(str(e) for e in list)
        str1 = "[{}]".format(str1)
        return str1 
    def stateOnList(self, list, label):
        for i in range (0, len(list)):
            if str(list[i].label()) == str(label):
                return i
        return -1
    def createAutomata(self):
        initialState = DeterministicState()
        initialState.setLabel(self.toAutomataLabel(self.root().firstPos()))
        stateList = [initialState]
        finalStates = []
        toVisit = [self.root().firstPos()]
        while(len(toVisit) > 0):
            print("toVisit: {}".format(toVisit))
            list = toVisit.pop(0)
            # Define state label
            str1 = self.toAutomataLabel(list)
            state = stateList[self.stateOnList(stateList, str1)]
            listsymbol = []
            print("Current state {}:".format(state.label()))
            for i in list:
                listsymbol.append(self.__dicSymbols[i])
            dicTo = {}
            for i in range(0, len(list)):
                symbol = listsymbol[i]
                if symbol not in dicTo:
                    dicTo[symbol] = self.__followPosTable[list[i]-1]
                else:
                    list = [dicTo[symbol], self.__followPosTable[list[i]-1]]
                    listunion = list(set().union(*list))
                    dicTo[symbol] = listunion
            for key in dicTo:
                if dicTo[key] != [0]:
                    pos = self.stateOnList(stateList, dicTo[key])
                    if  pos == -1:
                        dt = DeterministicState()
                        dt.setLabel(dicTo[key])
                        stateList.append(dt)
                        toVisit.append(dicTo[key])
                        print(state.label())
                        state.addTransition(key, dt)
                        transitions = state.getTransitions()
                        for key in transitions:
                            print("{} -> {}".format(key, transitions[key].label()))
                        # print(key, dt.label())
                    else:
                        dt = stateList[pos]
                        for key in transitions:
                            print("{} -> {}".format(key, transitions[key].label()))
                        print(state.label())
                        print(key, dt.label())
            state.setTransitions(dicTo)
            print(dicTo)
            if "#" in dicTo:
                finalStates.append(state)
        self.__DFA = DFA(stateList, initialState, finalStates)
def main():
    tree = SyntaxTree("a.b|c.d")
    print("Estado inicial: {}".format(tree.DFA().initialState().label()))
    print("All States")
    for i in tree.DFA().stateList():
        print(i.label())
    # Estados 
    # for i in tree.DFA().stateList():
    #     print("{}".format(i.label()))
    #     transitions = i.getTransitions()
    #     for key in transitions:
    #         print("{} -> {}".format(key, transitions[key].label()))
    print("Estado final: ", end="")
    for i in tree.DFA().finalStates():
        print(i.label())
    # tree = Tree("((a.b)|c.a)*|(a|b)*.c")
    # tree = Tree("(a.b)|c.a")
    # tree = Tree("(a.b)")
    # tree = Tree("c.a")
    # tree = Tree("(a|b)*.c")
    # tree = Tree("(a|b)*")
    # tree = Tree("a|b")
    # tree = Tree("b*")

if __name__ == "__main__":
    main()