import os

class Files:
    ROOT = os.path.join(os.getcwd())
    INPUT = os.path.join(ROOT, "inputs")
    OUTPUTS = os.path.join(ROOT, "outputs")
    OUTPUT_CSV = os.path.join(ROOT, "outputs","csv_files")
    ANY_OUTPUT_CSV = os.path.join(ROOT, "outputs","csv_files","automata{}.csv")
    OUTPUT_TABLE = os.path.join(ROOT, "outputs","table_result")
    ANY_OUTPUT_TABLE = os.path.join(ROOT, "outputs","table_result","automata{}.csv")
    CSV_1 = os.path.join(OUTPUT_CSV, "determinizacao1.csv")
    CSV_2 = os.path.join(OUTPUT_CSV, "determinizacao2.csv")
    CSV_3 = os.path.join(OUTPUT_CSV, "determinizacao3.csv")
    CSV_4 = os.path.join(OUTPUT_CSV, "determinizacao4.csv")
    TABLE_1 = os.path.join(OUTPUT_TABLE, "determinizacao1.csv")
    TABLE_2 = os.path.join(OUTPUT_TABLE, "determinizacao2.csv")
    TABLE_3 = os.path.join(OUTPUT_TABLE, "determinizacao3.csv")
    TABLE_4 = os.path.join(OUTPUT_TABLE, "determinizacao4.csv")
    IN_LEFT_FACTORING = os.path.join(INPUT, "left_factoring")
    OUT_LEFT_FACTORING = os.path.join(OUTPUTS, "left_factoring")
    IN_LEFT_FACTORING1 = os.path.join(IN_LEFT_FACTORING, "test1.txt")
    OUT_LEFT_FACTORING1 = os.path.join(OUT_LEFT_FACTORING, "test1.txt")