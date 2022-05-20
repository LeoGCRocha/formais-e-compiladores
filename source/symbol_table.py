import json 
from utils.helper import Helper


class SymbolTable:
    def __init__(self, code_file, config_file, output_file):
        self._code_file = code_file
        self.__config_file = config_file
        self.__output_file = output_file
        self.create_symbol_table_from_file()

    def create_symbol_table_from_file(self):
        arr = Helper.read_text_file(self._code_file)
        Symbol_Table = json.load(open(self.__config_file))
        reserved = Helper.adjustResverdWord(Symbol_Table['reserved']) + Symbol_Table['assignment'] + Symbol_Table['operators'] + Symbol_Table['delimiters']
        symbol_table = []
        symbol_table_hash_map = {}
        for line in arr:
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
                                    pass
                                else:
                                    if len(key) > key_size:
                                        key_size = len(key)
                            if key_size != 0:
                                cursor = cursor + key_size - 1
                                key_size = 0
                                if current != "":
                                    if current not in symbol_table_hash_map:
                                        if not Helper.is_float(current):
                                            symbol_table.append("{}".format(current))
                                            symbol_table_hash_map[current] = True
                                    current = ""
                            else:
                                current = current + line[cursor]
                    else:
                        if current != "":
                            if current not in symbol_table_hash_map:
                                if not Helper.is_float(current):
                                    symbol_table.append("{}".format(current))
                                    symbol_table_hash_map[current] = True
                            current = ""
                    cursor = cursor + 1
                    if (cursor == len(line)):
                        if current != "":
                            if current not in symbol_table_hash_map:
                                if not Helper.is_float(current):
                                    symbol_table.append("{}".format(current))
                                    symbol_table_hash_map[current] = True
                            current = ""
        Helper.write_csv_file(self.__output_file, "Symbol Table", symbol_table)