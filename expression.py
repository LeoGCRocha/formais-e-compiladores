import math
from operators import Operators as op

class Expression:
    @staticmethod
    def subExpressions(expression):
        expression = list(expression)
        index = Expression.findOperatorIndex(expression)
        try:
            openingParenthesesIndex = expression.index("(")
        except ValueError:
            openingParenthesesIndex = -1

        if (openingParenthesesIndex != -1):
            if index > openingParenthesesIndex:
                closingParenthesesIndex = Expression.findClosingParentheses(
                    expression,
                    openingParenthesesIndex
                )
                index = Expression.findOperatorIndex(
                    expression[closingParenthesesIndex:]
                ) + closingParenthesesIndex
                if index == math.inf:
                    if expression[-1] == op.STAR:
                        return expression[1:-2], None, op.STAR
                    else:
                        return Expression.subExpressions(expression[1:-1])
        elif index == math.inf:
            assert(expression[-1] == op.STAR)
            return expression[:-1], None, op.STAR
                    
        return expression[:index], expression[index+1:], expression[index]

    @staticmethod
    def findClosingParentheses(expression, openingParenthesesIndex):
        counter = 1
        for i in range(openingParenthesesIndex + 1, len(expression)):
            if expression[i] == ")":
                counter -= 1
            elif expression[i] == "(":
                counter += 1
            if counter == 0:
                return i

    @staticmethod
    def findOperatorIndex(expression):
        try:
            concatIndex = expression.index(op.CONCAT)
        except ValueError:
            concatIndex = math.inf

        try:
            orIndex = expression.index(op.OR)
        except ValueError:
            orIndex = math.inf
        
        return min(concatIndex, orIndex)