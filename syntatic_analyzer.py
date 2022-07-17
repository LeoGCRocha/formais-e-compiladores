import left_recursion as lr
import first_follow as fp
import parsingtable as pt
import copy
class SyntaticAnalyzer():
    def __init__(self, language_definition = "inputs/language_definition.txt", source = "inputs/source.txt"):
        self.__lanuage_definition = language_definition
        # self.__source = source
        self.__productions = {}
        self.prepareGrammar()
        self.__first = {}
        self.__follows = {}
        self.__nt = []
        self.__t = []
        self.__table = []
    def prepareGrammar(self):
        # Read language definition file and remove left recursion
        self.__productions = lr.eliminateLeftRecursion(self.__lanuage_definition)
        # Read production and remove left factoring
        # self.__productions = lr.eliminateLeftFactoring(self.__productions)
        # First & Follow
        arrayResults = fp.generateFirstAndFollow("outputs/language_definition.txt", self.__productions)
        # Save all first and follows
        self.__first = arrayResults[0]
        self.__follows = arrayResults[1]
        self.__nt = arrayResults[2]
        self.__t = arrayResults[3]
        # Parsing table
        self.__table = pt.generate_parse_table(self.__t, self.__nt, pt.adapt_grammar(copy.deepcopy(self.__productions)), \
            self.__first, self.__follows)
        pt.parseToCsv(self.__table, self.__nt, self.__t, "outputs/parse_table.csv")
    def getProductions(self):
        return self.__productions
if __name__ == "__main__":
    syntatic_analyzer = SyntaticAnalyzer("inputs/language_definition.txt", "inputs/source.txt")
    lr.dicToFile(syntatic_analyzer.getProductions(), "outputs/language_definition.txt")