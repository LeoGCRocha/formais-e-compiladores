from source.symbol_table import SymbolTable
from source.tokenizer import Tokenizer
from utils.files import Files


def main():
    st = SymbolTable(Files.INPUT, Files.CONFIG, Files.SYMBOL_TABLE)
    tokenizer = Tokenizer(
        Files.INPUT,
        Files.SYMBOL_TABLE,
        Files.CONFIG,
        Files.TOKENS
    )

if __name__ == "__main__":
    main()