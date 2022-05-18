import csv
def write_csv_file_symbol_table(filename, arr):
    with open(filename,'w') as file:
        for line in arr:
            file.write(line)
            file.write('\n')