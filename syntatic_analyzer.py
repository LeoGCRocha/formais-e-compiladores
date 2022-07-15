import left_recursion as lr
class SyntaticAnalyzer():
    def __init__(self, language_definition = "inputs/language_definition.txt", source = "inputs/source.txt"):
        self.__lanuage_definition = language_definition
        self.__source = source
        self.__productions = {}
        self.prepareGrammar()
    def prepareGrammar(self):
        # Read language definition file and remove left recursion
        self.__productions = lr.eliminateLeftRecursion(self.__lanuage_definition)
        # Read production and remove left factoring
        # self.__productions = lr.eliminateLeftFactoring(self.__productions)
    def getProductions(self):
        return self.__productions

if __name__ == "__main__":
    syntatic_analyzer = SyntaticAnalyzer("inputs/language_definition.txt", "inputs/source.txt")
    print(syntatic_analyzer.getProductions())
    lr.dicToFile(syntatic_analyzer.getProductions(), "outputs/language_definition.txt")