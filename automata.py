from abc import abstractmethod
from abc import ABC
import copy

# automata base class. Note that this class is abstract
class Automata(ABC):
    @abstractmethod
    def __init__(self, states, initial, final, name):
        self.name = name
        self.initial = initial
        self.final = final
        self.states = states
        self.deadState = DeterministicState()
    def initialState(sellf):
        pass
    def finalState(self):
        pass
    def stateList(self):
        pass

# deterministic finite automata
class DFA(Automata):
    def __init__(self, states = [], initial = None, final = [], name = "DFADefaultName"):
        # parent constructor
        super().__init__(states, initial, final, name)
        for state in states:
            for value in state.transitions().values():
                assert(not isinstance(value, list))

    # run the automata, given the input
    def run(self, inputString, trace = False):
        currentState = copy.deepcopy(self.__initial)
        for char in inputString:
            nextState = self.__step(currentState, char, trace)
            if (nextState == self.__deadState):
                break
            currentState = nextState

        finalState = self.__run(inputString, trace)
        if trace:
            if finalState in self.__final:
                print("accepted")
            else:
                print("rejected")
        return currentState

    # initial state
    def initialState(self):
        return self.initial
    # final states
    def finalStates(self):
        return self.final
    def stateList(self):
        return self.states
    # executes one step in the automata
    def __step(self, currentState, char, trace = False):
        try:
            nextState = currentState[char]
        except ValueError:
            nextState = self.__deadState
        if (trace):
            print(f"{currentState} -{char}-> {nextState}")
        return nextState

# non deterministic automata
class NFA(Automata):
    def __init__(self, states, name = "NFADefaultName"):
        super(Automata).__init__(self, states, name)

# base class for states. Note that this class is abstract
class BaseState(ABC):
    @abstractmethod
    def __init__(self):
        # assert(isinstance(transitions, dict))
        # self.transitions = transitions
        # unique id for each state
        self.__id = IdCounter.get()
        self.__label = None
        self.__transitions = {}

    @abstractmethod
    def addTransition(self, symbol, to):
        self.__transitions[symbol] = to

    def transitions(self):
        return self.__transitions

    def getTransitions(self):
        return self.__transitions
    
    def __repr__(self):
        return self.__id

    def __getitem__(self, symbol):
        return self.__transitions[symbol]
    
    def label(self):
        return self.__label

    def setTransitions(self):
        pass

    # TODO : Padronizar
    def setLabel(self, label):
        self.__label = label

class DeterministicState(BaseState):
    def __init__(self):
        super().__init__()
    
    def __setitem__(self, key, value):
        self.addTransition(key, value)

    def addTransition(self, symbol, to):
        return super().addTransition(symbol, to)

class NonDeterministicState(BaseState):
    def __init__(self, transitions = {}):
        super(BaseState).__init__(self, transitions)
        if (transitions.values()):
            assert(isinstance(transitions.values()[0], list))

    def addTransition(self, symbol, to):
        try:
            self.__transitions[symbol].append(to)
        except ValueError:
            self.__transitions[symbol] = [to]

# state of unknown type. Use this to create states without the need to know it's
# type. Then call convertToTypedState to convert this to a deterministic or
# non-deterministic state
class UnknownTypeState(NonDeterministicState):
    def __init__(self):
        super(NonDeterministicState).__init__(self, {})
    
    def __convertToDeterministicState(self):
        newState = DeterministicState()
        for key, value in self.transitions().items():
            newState.addTransition(key, value[0])
        return newState

    def __convertToNonDeterministicState(self):
        newState = NonDeterministicState()
        for key, value in self.transitions().items():
            for v in value:
                newState.addTransition(key, v)
        return newState

    def convertToTypedState(self):
        deterministic = True
        for value in self.transitions().values():
            if len(value) > 1:
                deterministic = False
                break
        if (deterministic):
            self.__convertToDeterministicState()
        else:
            self.__convertToNonDeterministicState()

# counter class
class IdCounter:
    counter = 0
    # generates unique id
    @staticmethod
    def get():
        r = IdCounter.counter
        IdCounter.counter += 1
        return r

def main():
    pass

if __name__ == "__main__":
    main()