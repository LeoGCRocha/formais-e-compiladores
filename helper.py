class Helper:
    @staticmethod
    def is_float(number):
        try:
            float(number)
            return True
        except:
            return False    
    @staticmethod
    def adjustResverdWord(reserved):
        return [x + " " for x in reserved]
    @staticmethod
    def read_text_file(filename):
        arr = []
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    arr.append(line.rstrip('\n').strip())
        except ValueError:
            print('File not found')
        return arr
    @staticmethod
    def write_csv_file_symbol_table(filename, arr):
        with open(filename,'w') as file:
            for line in arr:
                file.write(line)
                file.write('\n')