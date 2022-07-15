import csv
from syntaxtree import *
from prettytable import PrettyTable
from files import *

# Receive a list of regular expressions from a single file
# and create multiples .csv with the respectives ER as Automatas
def erToAF(file_path):
    # Create a list of regular expressions
    list_of_er = read_er(file_path)
    list_of_er = list(map(lambda x: prepare_expression(x), list_of_er))
    for er in list_of_er:
        err = "A expressao {}, nao eh valida.".format(er)
        assert(verify_expression(er)), err
    # Create a list of automata
    automata_list = []
    number = 0
    for er in list_of_er:
        syntax_tree = SyntaxTree(er)
        automata_list.append(syntax_tree.getAutomata())
        # Save automata on .csv file
        file_path = Files.ANY_OUTPUT_CSV.format(str(number))
        automata_to_csv(file_path, automata_list[-1], syntax_tree.getListOfSymbols())
        csv_to_table(file_path, Files.ANY_OUTPUT_TABLE.format(str(number)))
        number += 1
        
def read_er(file_path):
    er = []
    file = open(file_path, "r")
    with file as file:
        for line in file:
            er.append(line.rstrip())
    return er

def automata_to_csv(file_path, automata, list_of_symbols):
    header = ["δ"]
    for x in list_of_symbols:
        header.append(x)   
    data = []
    for i in automata.states:
        dataToAdd = [i.label]
        if i.label == automata.initial.label:
            finalState = False
            for final in automata.final:
                if final.label == i.label:
                    finalState = True
            if finalState:
                str = "{}{}{}".format("->", i.label, "*")
                dataToAdd[0] = str
            else:
                str = "{}{}".format("->", i.label)
                dataToAdd[0] = str
        else:
            for final in automata.final:
                if final.label == i.label:
                    str = "{}{}".format("*", i.label)
                    dataToAdd[0] = str
        for _ in range (0,len(header)-1):
            dataToAdd.append([])
        transitions = i.transitions
        for key in transitions:
            position = 0
            for x in range(1, len(header)):
                if key == header[x]:
                    position = x
            dataToAdd[position].append(transitions[key].label)
        data.append(dataToAdd)
    with open(file_path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for d in data:
            writer.writerow(d)

def csv_to_table(csv_file, outpath):
    table = PrettyTable()
    file = open(csv_file)
    #create header of table
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    table.field_names = header
    #create rows of table
    for row in csv_reader:
        table.add_row(row)
    file.close()
    with open(outpath, 'w') as file:
        file.write(table.get_string())

def tokens_to_txt(outpath, tokens):
    with open(outpath, "w") as file:
        for token in tokens:
            file.write(f"< {token[0]}, {token[1]} >\n")

def symbol_table_to_csv(outpath, table):
    with open(outpath, "w") as file:
        file.write("lexeme, logical meaning\n")
        for l in table:
            file.write(f"{l[0]}, {l[1]}\n")

def language_read(file_path):
    lines = []
    with open(file_path, "r") as file:
        for line in file:
            lines.append(
                list(map(
                    lambda x : x.strip(), 
                    line.rstrip().split("->")
                ))
            )
    language = {
        line[0] : list(map(
            lambda x : x.strip(), 
            line[1].split(",")
        )) for line in lines
    }
    
    return language

def language_write(file_path, language):
    with open(file_path, "w") as file:
        for key, values in language.items():
            file.write(f"{key} -> ")
            file.write(", ".join(["".join(value) for value in values]) + "\n")