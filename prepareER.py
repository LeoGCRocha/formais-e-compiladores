import string


def resolve_dependencies():
    language = {}
    lines = []

    with open("inputs/language.txt", "r") as file:
        lines = file.readlines()
        lines = list(map(lambda x : x.strip(), lines))

    definitions = []
    for line in lines:
        definitions.append(list(map(lambda x: x.strip(), line.split("->"))))

    for key, value in definitions:
        while (1):
            has_quotation = "\"" in value
            if not has_quotation:
                break

            if has_quotation:
                opening_quotation_index = value.index("\"")
                closing_quotation_index = value[opening_quotation_index + 1:].index("\"") + opening_quotation_index + 1
                try:
                    definition = value[opening_quotation_index + 1 : closing_quotation_index]
                    to = language[definition]
                except KeyError:
                    print(f"mal formed language. \"{definition}\" is not defined.")
                    exit()
                value = value[:opening_quotation_index] + "(" + to + ")" + value[closing_quotation_index + 1:]
        
        language[key] = prepare_expression(value)

    language = { key : prepare_expression(value) for key, value in language.items()}
    print(language)

def verify_expression(expression):
    valid_inputs = string.ascii_lowercase + string.digits + '|.*?()'
    ant = ' '
    parent_level = 0
    
    for i in range(0,len(expression)):
        char = expression[i]
        if char in valid_inputs:
            if i > 1:
                ant = expression[i-1]
                if (ant in '(|.' and char in '|.*?)') or (ant in '?*' and char in '?*') or (ant in '|.' and char == ')') or (ant == "*" and char == '('):
                    return False
                if (i == (len(expression)-1) and char in '|.'):
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
    latest_parenteses = -1
    i = 0
    while i < len(expression_final): 
        char = expression[i]
        
        if char == '(':
            latest_parenteses = i
        
        if i > 0:
            ant = expression[i-1] 
            if (isinstance(ant, int) or ant.isalpha()) and (char == '?'):
                str1 = expression_final[:i+concat-1]
                strmed = expression_final[i+concat-1]
                str2 = expression_final[i+1+concat:]
                expression_final = str1 + '(' + strmed + '|&)' + str2
                concat +=3
            if (ant == ")") and (char == '?'):
                latest_parenteses += concat
                expression_final = expression_final[0:latest_parenteses] + "(" + expression_final[latest_parenteses:i] + '|&)' + expression_final[i+1+concat:]
                concat +=4

        concat = 0
        expression = expression_final
        i +=1
    
    #Resolve Concatenações implicitas
    for i in range(0,len(expression)): 
        char = expression[i]
        if i > 0:
            ant = expression[i-1]
            if (isinstance(ant, int) or ant.isalpha() or ant in "&*") and (isinstance(char, int) or char.isalpha() or char == "&*ε") \
            or (ant == ")") and (isinstance(char, int) or char.isalpha() or char == "&")\
            or (isinstance(ant, int) or ant.isalpha() or ant in '*&)') and (char == "("):
                str1 = expression_final[:i+concat]
                str2 = expression_final[i+concat:]
                expression_final = str1 + '.' + str2
                concat +=1
    return expression_final

def main():
    resolve_dependencies()

if __name__ == "__main__":
    main()

