import txt_modules as txt
import csv_modules as csv
arr = txt.read_text_file('dummy_data/cd/example1.txt')
def create_symbol_table_from_file(code_file, command_reserved_keys, reserved_keys):
    last_id = 0
    arr = txt.read_text_file(code_file)
    reserved_command = txt.read_text_file_keys(command_reserved_keys)
    reserved_keys = txt.read_text_file_keys(reserved_keys)
    symbol_table = []
    symbol_table_hash_map = {}
    for line in arr:
        # line command
        if line in reserved_command: 
            pass
        else:
            current = ""
            cursor = 0
            while(cursor < len(line)):
                if line[cursor] != " ":
                    key_size = 0 
                    for key in reserved_keys:
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
                                symbol_table.append("{}#id{}".format(current, last_id))
                                last_id+=1
                                symbol_table_hash_map[current] = last_id
                            current = ""
                    else:
                        current = current + line[cursor]
                cursor = cursor + 1
                if (cursor == len(line)):
                    if current != "":
                        if current not in symbol_table_hash_map:
                            symbol_table.append("{}#id{}".format(current, last_id))
                            last_id+=1
                            symbol_table_hash_map[current] = last_id
                        current = ""
    csv.write_csv_file_symbol_table('dummy_data/cd/generated_files/symbol_table_1.csv', symbol_table)
create_symbol_table_from_file('dummy_data/cd/example1.txt', 'dummy_data/cd/commands_reserved_keys.txt', 'dummy_data/cd/reserved_keys.txt')