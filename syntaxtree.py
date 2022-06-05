from node import Node
from expression import Expression
from operators import Operators as OP
from prepareER import *
from automataState import *
from automata import *

class SyntaxTree:
    def __init__(self, expression):
        self.__expression = expression
        self.__enumerateCount = 1
        self.__root = Node(OP.CONCAT, self.__build(expression), Node(OP.END))
        self.__dicSymbols = {}
        self.__listOfSymbols = []
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

    def getListOfSymbols(self):
        return self.__listOfSymbols

    def numerateLeaves(self, node):
        if node.isLeaf():
            node.setNum(self.__enumerateCount)
            self.__enumerateCount = self.__enumerateCount + 1
            self.__dicSymbols[node.num()] = node.symbol()
            if node.symbol() not in self.__listOfSymbols and node.symbol() != "#":
                self.__listOfSymbols.append(node.symbol())
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
                if node.left() != None:
                    if node.left().nullable() == None:
                        self.setNodes(node.left())
                if node.right() != None:
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
                    if node.left() != None and node.right() != None:
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
                    node.setLastPos(node.left().lastPos())

    def prepareFollowPos(self):
        for _ in range(1, self.__enumerateCount):
            self.__followPosTable.append([])
        self.__followPosTable[-1] = [0]
    def setFollowPos(self, node):
        # from leaves to root
        if not node.isLeaf() and node.symbol() != OP.END:
            if node.left() != None:
                self.setFollowPos(node.left())
            if node.right() != None:
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
                for i in node.lastPos():
                    listc1c2 = [self.__followPosTable[i-1], node.firstPos()]
                    self.__followPosTable[i-1] = list(set().union(*listc1c2))
    def root(self):
        return self.__root
    def getAutomata(self):
        return self.__DFA
    def DFA(self):
        return self.__DFA
    def followPosTable(self):
        return self.__followPosTable
    def toAutomataLabel(self, listArray):
        str1 = ', '.join(str(e) for e in listArray)
        str1 = "[{}]".format(str1)
        return str1 
    def stateOnList(self, listArray, label):
        for i in range (0, len(listArray)):
            if str(listArray[i].label) == str(label):
                return i
        return -1
    def createAutomata(self):
        initialState = DeterministicState({})
        initialState.setLabel(self.toAutomataLabel(self.root().firstPos()))
        stateList = [initialState]
        finalStates = []
        toVisit = [self.root().firstPos()]
        while(len(toVisit) > 0):
            listArray = toVisit.pop(0)
            # Define state label
            str1 = self.toAutomataLabel(listArray)
            state = stateList[self.stateOnList(stateList, str1)]
            listsymbol = []
            for i in listArray:
                listsymbol.append(self.__dicSymbols[i])
            dicTo = {}
            i = 0
            while i < len(listArray):
                symbol = listsymbol[i]
                if symbol not in dicTo:
                    dicTo[symbol] = self.__followPosTable[listArray[i]-1]
                else:
                    listArray = [dicTo[symbol], self.__followPosTable[listArray[i]-1]]
                    listunion = list(set().union(*listArray))
                    dicTo[symbol] = listunion
                i+=1
            for key in dicTo:
                if dicTo[key] != [0]:
                    pos = self.stateOnList(stateList, dicTo[key])
                    if  pos == -1:
                        dt = DeterministicState({})
                        dt.label = dicTo[key]
                        stateList.append(dt)
                        toVisit.append(dicTo[key])
                        state.addTransition(key, dt)
                    else:
                        dt = stateList[pos]
                        state.addTransition(key, dt)
            if "#" in dicTo:
                if self.stateOnList(finalStates, state.label) == -1:
                    finalStates.append(state)
                if state.label == initialState.label and self.stateOnList(finalStates, state.label) == -1:
                    finalStates.append(state)
        self.__DFA = DFA(stateList, initialState, finalStates, "DFADefaultName")
    def printAutomata(self):
        print("Estado inicial: {}".format(self.__DFA.initialState.label))
        for i in self.__DFA.stateList():
            transitions = i.getTransitions()
            print("Estado: {}".format(i.label))
            for key in transitions:
                print("{} -> {}".format(key, transitions[key].label))
        print("Estado final: ", end="")
        for i in self.__DFA.finalStates():
            print(i.label, end="")        
        print()
    