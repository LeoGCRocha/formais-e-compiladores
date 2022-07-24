import left_recursion as lr
import first_follow as fp
import parsingtable as pt
import left_factoring as lf
import stack_buffer as sb
import copy
import prepareER as pre
class SyntaticAnalyzer():
    def __init__(self, language_definition = "inputs/language_definition.txt", source = "inputs/source.txt"):
        self.__language_definition = language_definition
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
        self.__productions = lr.eliminateLeftRecursion(self.__language_definition)
        # Read production and remove left factoring
        results = pre.resolve_dependencies("inputs/language.txt")
        new_array = []
        for i in results[1]:
            new_array.append(i[0])
        multiple_symbols = list(self.__productions.keys()) + new_array + results[2]
        self.__productions = lf.do_left_factoring(self.__productions, [])
        # First & Follow
        lr.dicToFile(self.getProductions(), "outputs/language_definition.txt")
        arrayResults = fp.generateFirstAndFollow("outputs/language_definition.txt", self.__productions)
        # Save all first and follows
        self.__first = arrayResults[0]
        self.__follows = arrayResults[1]
        self.__nt = arrayResults[2]
        self.__t = arrayResults[3]
        self.__t.append("$")
        self.__table = pt.generate_parse_table(self.__t, self.__nt, pt.adapt_grammar(copy.deepcopy(self.__productions), self.__t), \
            self.__first, self.__follows)
        pt.parseToCsv(self.__table, self.__nt, self.__t, "outputs/parse_table.csv")
        self.validate()
    def getProductions(self):
        return self.__productions
    def validate(self):
        nicolas_vans = sb.readTokensAndPrepare("outputs/tokens.txt")
        isValid = sb.validateCode(self.getFirstSymbol(), sb.readTokensAndPrepare("outputs/tokens.txt"), \
            self.__nt, self.__t, self.__table)
        if isValid:
            print("Codigo compilado com sucesso.")
        else:
            print("O código não segue o padrão definindo na GLC.")
    def getFirstSymbol(self):
        with open(self.__language_definition) as f:
            lines = f.readlines()[0][0]
            return lines
syntatic_analyzer = SyntaticAnalyzer("inputs/language_definition.txt", "inputs/source.txt")