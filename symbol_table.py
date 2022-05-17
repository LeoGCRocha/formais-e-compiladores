from venv import create
import txt_modules as txt
import csv_modules as csv
arr = txt.read_text_file('dummy_data/cd/example1.txt')
def isVariable(word):
    number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for a in word:
        if a not in number_list:
            return True
    return False
def create_symbol_table_from_file(code_file, reserved_keys_file):
    last_id = 0
    arr = txt.read_text_file(code_file)
    arr_reserved_keys = txt.read_text_file(reserved_keys_file)
    symbol_table_hash_map = {}
    symble_table = []
    for line in arr:
        line_splited = line.split(' ')
        for word in line_splited:
            if word not in arr_reserved_keys:
                if word not in symbol_table_hash_map:
                    if isVariable(word):
                        symbol_table_hash_map[word] = "id{}".format(last_id)
                        symble_table.append("{}#{}".format(word, last_id))
                        last_id+=1
                else:
                    if isVariable(word):
                        symble_table.append("{}#{}".format(word, last_id))
                        last_id+=1
    # save on .csv
    csv.write_csv_file_symbol_table('dummy_data/cd/generated_files/symbol_table_1.csv', symble_table)
create_symbol_table_from_file('dummy_data/cd/example1.txt', 'dummy_data/cd/example1_reserved_keys.txt')