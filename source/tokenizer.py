from dataclasses import dataclass
from enum import Enum, auto
from typing import Union
from utils.helper import Helper
import json, csv


class Tokenizer:
	def __init__(self, input_file, symbol_table_file, config_file, output_file):
		self.tokens = []
		self.symbol_table = []

		self.char_to_token_type = {}
		self.token_type_to_char = {
			token_type : [] for token_type in Token_type
		}

		self.__config(config_file)
		self.__load_symbol_table(symbol_table_file)
		self.tokenize(input_file)
		self.__write_tokens_to_file(output_file)

	def __write_tokens_to_file(self, output_file):
		tokens = list(map(
			lambda x: f"{x.type.name}, {str(x.value)}", self.tokens
		))
		Helper.write_csv_file(output_file, "Token type, value", tokens)

	def __load_symbol_table(self, filename):
		with open(filename) as file:
			csvreader = csv.reader(file)
			header = next(csvreader)
			for row in csvreader:
				self.symbol_table.extend(row)
	
		for symbol in self.symbol_table:
			self.char_to_token_type[symbol] = Token_type.ID
			self.token_type_to_char[Token_type.ID].append(symbol)

	def __config(self, filename):
		file = json.load(open(filename))
		try:
			for r in file["reserved"]:
				self.char_to_token_type[r] = Token_type.RESERVED
				self.token_type_to_char[Token_type.RESERVED].append(r)
			for a in file["assignment"]:
				self.char_to_token_type[a] = Token_type.ASSIGNMENT
				self.token_type_to_char[Token_type.ASSIGNMENT].append(a)
			for o in file["operators"]:
				self.char_to_token_type[o] = Token_type.OPERATOR
				self.token_type_to_char[Token_type.OPERATOR].append(o)
			for d in file["delimiters"]:
				self.char_to_token_type[d] = Token_type.DELIMITER
				self.token_type_to_char[Token_type.DELIMITER].append(d)
		except KeyError:
			print("bad tokenizer config file.")

	# Isolates each lexeme
	# example:
	# [["var=a+b-c"]] -> ["var", "=", "a", "+", "b", "-", "c"]
	def __isolate_lexemes(self, filename):
		file_text = [open(filename, "r").read()]
		
		for token_type in (
			Token_type.OPERATOR, Token_type.ASSIGNMENT, Token_type.DELIMITER
		):
			while(True):
				splitted = False
				for i in range(len(file_text)):
					string = file_text[i]
					# search for lexeme of 'token_type'
					for word in self.token_type_to_char[token_type]:
						# found lexeme
						if word != string and word in string:
							# splits the current string
							substrings = string.split(word, 1)
							file_text.pop(i)
							# inserts splitted string in the file_text again
							for new_substring in (
								substrings[1], word, substrings[0]
							):
								if new_substring:
									file_text.insert(
										i, new_substring.strip()
									)
									splitted = True
						# only split one string per loop.
						if splitted:
							break
					else:
						continue
					break
				if (not splitted):
					break

		return file_text

	# classifies each lexeme on the list.
	def __tokenize(self, lexemes):
		for lexeme in lexemes:
			try:
				token = Token(self.char_to_token_type[lexeme], lexeme)
			except KeyError:
				if Helper.is_float(lexeme):
					token = Token(Token_type.CONST, lexeme)
				else:
					token = Token(Token_type.UNKNOWN, lexeme)
			self.tokens.append(token)
		return self.tokens

	def tokenize(self, file):
		lexemes = self.__isolate_lexemes(file)
		self.__tokenize(lexemes)

		# sets ID tokens value to index symbol_table
		# Token<ID, a> -> Token<ID, indexof(a)>
		for token in self.tokens:
			if token.type == Token_type.ID:
				token.value = self.symbol_table.index(token.value)

# enumeration of all token types
class Token_type(Enum):
	OPERATOR = auto()
	ASSIGNMENT = auto()
	DELIMITER = auto()
	#PARENTHESES = auto()
	#BRACKETS = auto()
	#CURLY_BRACKETS = auto()
	RESERVED = auto()
	ID = auto()
	CONST = auto()
	#LITERAL = auto()
	UNKNOWN = auto()

# token data type
@dataclass
class Token:
	type: Token_type
	value: Union[int, str, float]

	def __repr__(self):
		return f"Token<{self.type.name}, {self.value}>"
