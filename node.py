class Node:
    def __init__(self,
        symbol,
        father = None,
        left = None,
        right = None,
        num = None,
        firstPos = [],
        endPos = [],
        nullable = None
    ):
        self.__symbol = symbol
        self.__right = right
        self.__left = left
        self.__num = num
        self.__firstPos = firstPos
        self.__endPos = endPos
        self.__nullable = nullable
        self.__father = father
    def symbol(self):
        return self.__symbol
    def right(self):
        return self.__right
    def left(self):
        return self.__left
    def setRight(self, right):
        self.__right = right
        self.__right.setFather(self)
    def setLeft(self, left):
        self.__left = left
        self.__left.setFather(self)
    def isLeaf(self):
        return self.__left == None and self.__right == None
    def num(self):
        return self.__num
    def setNum(self, num):
        self.__num = num
    def firstPos(self):
        return self.firstPos
    def endPos(self):
        return self.endPos
    def firstPos(self):
        return self.__firstPos
    def setFirstPos(self, firstPos):
        self.__firstPos = firstPos
    def nullable(self):
        return self.__nullable
    def setNullable(self, nullable):
        self.__nullable = nullable
    def father(self):
        return self.__father
    def setFather(self, father):
        self.__father = father