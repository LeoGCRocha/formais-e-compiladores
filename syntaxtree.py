from node import Node
from expression import Expression
from operators import Operators as OP

class SyntaxTree:
    def __init__(self, expression):
        self.__expression = expression
        self.enumerateCount = 1
        self.__root = Node(OP.CONCAT, self.__build(expression), Node("#"))

    def __build(self, expression):
        first, last, operator = Expression.subExpressions(expression)
        node = Node(operator)
        if (operator == "*"):
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
            node.setNum(self.enumerateCount)
            self.enumerateCount = self.enumerateCount + 1
        else:
            if node.left() != None:
                self.numerateLeaves(node.left())
            if node.right() != None:
                self.numerateLeaves(node.right())

    def setNodes(self, node):
        if node != None:
            if node.isLeaf():
                # A leaf labeled &
                if node.symbol() == "&":
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
                if node.symbol() == "|":
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
                elif node.symbol() == ".":
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
                elif node.symbol() == "*":
                    # A star-node n = c1*
                    # node c1
                    node.setNullable(True)
                    # firstpos(c1)
                    node.setFirstPos(node.left().firstPos())
                    node.setLastPos(node.left().firstPos())
    
    def root(self):
        return self.__root

def main():
    tree = SyntaxTree("a.b|c.d")
    tree.numerateLeaves(tree.root())
    tree.setNodes(tree.root())
    print(tree.root().firstPos())
    print(tree.root().lastPos())
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