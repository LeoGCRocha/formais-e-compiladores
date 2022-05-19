import re
import txt_modules as txt
import csv_modules as csv
import json 
def adjustReservedWord(reserved_word_list):
    for i in range(0, len(reserved_word_list)):
        reserved_word_list[i] = reserved_word_list[i] + " "
    return reserved_word_list
def create_symbol_table_from_file(code_file):
    last_id = 0
    arr = txt.read_text_file(code_file)
    arr = txt.read_text_file('dummy_data/cd/example1.txt')
    Symbol_Table = json.load(open("config.json"))
    reserved = adjustReservedWord(Symbol_Table['reserved']) + Symbol_Table['assignment'] + Symbol_Table['operators']
    symbol_table = []
    symbol_table_hash_map = {}
    for line in arr:
        # line command
        if line in reserved:
            pass
        else:
            current = ""
            cursor = 0
            while(cursor < len(line)):
                if line[cursor] != " ":
                        key_size = 0 
                        for key in reserved:
                            result = line[cursor:].find(key) + cursor
                            if result != cursor:
                                pass # not correct key
                            else:
                                if len(key) > key_size:
                                    key_size = len(key)
                        if key_size != 0:
                            cursor = cursor + key_size - 1
                            key_size = 0
                            if current != "":
                                if current not in symbol_table_hash_map:
                                    if not current.isnumeric():
                                        symbol_table.append("{}".format(current))
                                        symbol_table_hash_map[current] = True
                                current = ""
                        else:
                            current = current + line[cursor]
                else:
                    if current != "":
                        if current not in symbol_table_hash_map:
                            if not current.isnumeric():
                                symbol_table.append("{}".format(current))
                                symbol_table_hash_map[current] = True
                        current = ""
                cursor = cursor + 1
                if (cursor == len(line)):
                    if current != "":
                        if current not in symbol_table_hash_map:
                            if not current.isnumeric():
                                symbol_table.append("{}".format(current))
                                symbol_table_hash_map[current] = True
                        current = ""
    csv.write_csv_file_symbol_table('dummy_data/cd/generated_files/symbol_table_1.csv', symbol_table)
create_symbol_table_from_file('dummy_data/cd/example1.txt')