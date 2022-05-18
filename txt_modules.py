def read_text_file(filename):
    """
    Reads a text file and returns a array of string to each line.
    """
    arr = []
    try:
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                arr.append(line.rstrip('\n').strip())
    except ValueError:
        print('File not found')
    return arr
def read_text_file_keys(filename):
    """
    Reads a text file and returns a array of string to each line.
    """
    arr = []
    try:
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                arr.append(line.rstrip('\n').strip()[:-1])
    except ValueError:
        print('File not found')
    return arr