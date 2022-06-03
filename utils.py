def read_er(file_path):
    er = []
    file = open(file_path, "r")
    with file as file:
        for line in file:
            er.append(line.rstrip())
    return er