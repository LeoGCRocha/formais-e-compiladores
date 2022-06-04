import csv
from syntaxtree import *
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