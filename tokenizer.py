from dataclasses import dataclass
from enum import Enum, auto
from typing import Union
from helper import Helper
import json


class Tokenizer:
	def __init__(self, config_file):
		self.tokens = []
		
		self.operators = []
		self.reserved = []
		self.assignment = []

		self.char_to_token_type = {}
		self.token_type_to_char = {
			token_type : [] for token_type in Token_type
		}

		self.__build_char_token_dicts(json.load(open(config_file)))

	def __build_char_token_dicts(self, file):
		for r in file["reserved"]:
			self.char_to_token_type[r] = Token_type.RESERVED
			self.token_type_to_char[Token_type.RESERVED].append(r)
		for a in file["assignment"]:
			self.char_to_token_type[a] = Token_type.ASSIGNMENT
			self.token_type_to_char[Token_type.ASSIGNMENT].append(a)
		for o in file["operators"]:
			self.char_to_token_type[o] = Token_type.OPERATOR
			self.token_type_to_char[Token_type.OPERATOR].append(o)

		self.char_to_token_type["{"] = Token_type.CURLY_BRACKETS
		self.char_to_token_type["}"] = Token_type.CURLY_BRACKETS
		self.char_to_token_type["("] = Token_type.PARENTHESES
		self.char_to_token_type[")"] = Token_type.PARENTHESES
		self.char_to_token_type["["] = Token_type.BRACKETS
		self.char_to_token_type["]"] = Token_type.BRACKETS
		self.token_type_to_char[Token_type.PARENTHESES].extend([")", "("])
		self.token_type_to_char[Token_type.BRACKETS].extend(["[", "]"])
		self.token_type_to_char[Token_type.CURLY_BRACKETS].extend(["{", "}"])
	
	def __search_and_split(self, token_type):
		while True:
			splitted = False

			for i in range(len(self.file_text)):
				string = self.file_text[i]
				for word in self.token_type_to_char[token_type]:
					if word in string:
						substrings = string.split(word, 1)
						string

			if (not splitted):
				break

	def tokenize(self, file):
		self.file_text = [open(file, "r").read()]

		while(True):
			splitted = False
			for i in range(len(self.file_text)):
				string = self.file_text[i]
				for token_type in (
					Token_type.OPERATOR, 
					Token_type.ASSIGNMENT,
					Token_type.PARENTHESES,
					Token_type.BRACKETS,
					Token_type.CURLY_BRACKETS,
				):
					for word in self.token_type_to_char[token_type]:
						if word != string and word in string:
							substrings = string.split(word, 1)
							self.file_text.pop(i)
							for new_substring in (
								substrings[1], word, substrings[0]
							):
								if new_substring:
									self.file_text.insert(
										i, new_substring.strip()
									)
									splitted = True
						if splitted:
							break
					else:
						continue
					break
				else:
					continue
				break
			if (not splitted):
				break

		for lexem in self.file_text:
			try:
				token = Token(self.char_to_token_type[lexem], lexem)
			except KeyError:
				if Helper.is_float(lexem):
					token = Token(Token_type.CONST, lexem)
				else:
					token = Token(Token_type.UNKNOWN, lexem)
			self.tokens.append(token)
		print(self.tokens)



# enumeration of all token types
class Token_type(Enum):
	OPERATOR = auto()
	ASSIGNMENT = auto()
	PARENTHESES = auto()
	BRACKETS = auto()
	CURLY_BRACKETS = auto()
	RESERVED = auto()
	ID = auto()
	CONST = auto()
	LITERAL = auto()
	UNKNOWN = auto()

# token data type
@dataclass
class Token:
	type: Token_type
	value: Union[int, str, float]

	def __repr__(self):
		return f"Token<{self.type.name}, {self.value}>"

def test():
	tokenizer = Tokenizer("tokenizerconfig.json")
	tokenizer.tokenize("input.txt")

if __name__ == "__main__":
	test()