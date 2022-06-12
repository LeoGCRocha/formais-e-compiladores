import csv
from syntaxtree import *
from prettytable import PrettyTable
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