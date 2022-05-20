from enum import Enum
import os

class Files:
	ROOT = os.path.join(os.getcwd(), "files")
	CONFIG = os.path.join(ROOT, "config", "config.json")
	INPUT = os.path.join(ROOT, "input.txt")
	RESULTS = os.path.join(ROOT, "results")
	SYMBOL_TABLE = os.path.join(RESULTS, "symbol_table.csv")
	TOKENS = os.path.join(RESULTS, "tokens.csv")

	def __repr__(self):
		return self.value