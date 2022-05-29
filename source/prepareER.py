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
    for i in range(0,len(expression)): 
        char = expression[i]
        if i > 0:
            ant = expression[i-1] 
            if (isinstance(ant, int) or ant.isalpha()) and (char == '?'):
                str1 = expression_final[:i+concat]
                str2 = expression_final[i+1+concat:]
                expression_final = str1 + '|&' + str2
                concat +=1
    concat = 0
    expression = expression_final
    
    for i in range(0,len(expression)): 
        char = expression[i]
        if i > 0:
            ant = expression[i-1]
            if (isinstance(ant, int) or ant.isalpha() or ant in "&*") and (isinstance(char, int) or char.isalpha() or char == "&*"):
                str1 = expression_final[:i+concat]
                str2 = expression_final[i+concat:]
                expression_final = str1 + '.' + str2
                concat +=1

   
    return expression_final


#print(verify_expression("a.b|c|d"))
#print(verify_expression("a.b|c|d*"))
#print(verify_expression("a..b|c|d*"))
#print(verify_expression("a.(b|c)|d*"))
#print(verify_expression("a.(b|c))|d*"))   
print(prepare_expression("ab|cd|def"))
print(prepare_expression("a.b*ec?"))
print(prepare_expression("a|b?cd?"))