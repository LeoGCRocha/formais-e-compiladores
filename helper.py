import csv
class Helper:
    @staticmethod
    def is_float(number):
        try:
            float(number)
            return True
        except:
            return False    
    def adjustResverdWord(reserved):
        return [x + " " for x in reserved]
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
    def write_csv_file_symbol_table(filename, arr):
        with open(filename,'w') as file:
            for line in arr:
                file.write(line)
                file.write('\n')