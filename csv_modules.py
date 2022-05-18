import csv
def write_csv_file_symbol_table(filename, arr):
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Symbol", "Id"])
        for line in arr:
            writer.writerow(line.split('#'))