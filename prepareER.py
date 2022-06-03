import string

def verify_expression(expression):
    valid_inputs = string.ascii_lowercase + string.digits + '|.*?()'
    ant = ' '
    parent_level = 0
    
    for i in range(0,len(expression)-1):
        char = expression[i]
        if char in valid_inputs:
            if i > 1:
                ant = expression[i-1]
                if (ant in '(|.' and char in '|.*?)') or (ant in '?*' and char in '?*'):
                    return False
            if char == '(':
                parent_level +=1
            if char == ')':
                if parent_level - 1 < 0: 
                    return False
                parent_level -=1
        else:
            return False
    if parent_level != 0:
        return False
    else:
        return True

    
def prepare_expression(expression):
    expression = ''.join(expression.split())
    expression_final = expression
    ant = ''
    concat = 0
    
    # Trata expressoes como [0-1]+ ou [a-z]*
    if expression[0] == "[":
        expression_final = ''
        if expression[1] in string.digits:
            for i in range(string.digits.index(expression[1]),string.digits.index(expression[3])+1):
                if i == string.digits.index(expression[1]):
                    expression_final = string.digits[i] 
                else:
                    expression_final = expression_final+'|'+ string.digits[i]
            
            if expression[5] == '*':
                    expression_final = expression_final+'|'+ '&'
            return expression_final

        if expression[1] in string.ascii_lowercase:
            for i in range(string.ascii_lowercase.index(expression[1]),string.ascii_lowercase.index(expression[3])+1):
                if i == string.ascii_lowercase.index(expression[1]):
                    expression_final = string.ascii_lowercase[i] 
                else:
                    expression_final = expression_final+'|'+ string.ascii_lowercase[i]
            
            if expression[5] == '*':
                    expression_final = expression_final+'|'+ '&'
            return expression_final

    #Trata ER regulares

    #Resolve ?
    for i in range(0,len(expression)): 
        char = expression[i]
        if i > 0:
            ant = expression[i-1] 
            if (isinstance(ant, int) or ant.isalpha()) and (char == '?'):
                str1 = expression_final[:i+concat-1]
                strmed = expression_final[i+concat-1]
                str2 = expression_final[i+1+concat:]
                expression_final = str1 + '(' + strmed + '|&)' + str2
                concat +=3
    concat = 0
    expression = expression_final
    
    #Resolve Concatenações implicitas
    for i in range(0,len(expression)): 
        char = expression[i]
        if i > 0:
            ant = expression[i-1]
            if (isinstance(ant, int) or ant.isalpha() or ant in "&*") and (isinstance(char, int) or char.isalpha() or char == "&*") \
            or (ant == ")") and (isinstance(char, int) or char.isalpha())\
            or (isinstance(ant, int) or ant.isalpha()) and (char == "("):
                str1 = expression_final[:i+concat]
                str2 = expression_final[i+concat:]
                expression_final = str1 + '.' + str2
                concat +=1

    return expression_final