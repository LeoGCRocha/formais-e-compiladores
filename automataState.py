from abc import ABC, abstractmethod


# base class for states. Note that this class is abstract
class BaseState(ABC):
    @abstractmethod
    def __init__(self, transitions):
        assert(isinstance(transitions, dict))
        self.transitions = transitions
        self.id = IdCounter.get()
        self.label = None
        self.meaning = []

    @abstractmethod
    def addTransition(self, symbol, to):
        pass
    
    def __repr__(self):
        if (self.label):
            return f"{self.label}"
        else:
            return f"<Stid: {self.id}>"

    def __getitem__(self, symbol):
        return self.transitions[symbol]
    
    def __setitem__(self, symbol, to):
        self.addTransition(symbol, to)
    
    def label(self):
        return self.label

    # TODO : Padronizar
    def setLabel(self, label):
        self.label = label

class DeterministicState(BaseState):
    def __init__(self, transitions):
        super().__init__(transitions)
        for value in self.transitions.values():
            assert(not isinstance(value, list))

    def addTransition(self, symbol, to):
        self.transitions[symbol] = to

class NonDeterministicState(BaseState):
    def __init__(self, transitions):
        super().__init__(transitions)
        for value in self.transitions.values():
            assert(isinstance(value, list))

    def addTransition(self, symbol, to):
        try:
            self.transitions[symbol].append(to)
        except KeyError:
            self.transitions[symbol] = [to]
    
    def addTransitions(self, symbol, to_list):
        assert(isinstance(to_list, list))
        for to in to_list:
            self.addTransition(symbol, to)

# state of unknown type. Use this to create states without the need to know it's
# type. Then call convertToTypedState to convert this to a deterministic or
# non-deterministic state
class UnknownTypeState(NonDeterministicState):
    def __init__(self):
        super().__init__(self, {})
    
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