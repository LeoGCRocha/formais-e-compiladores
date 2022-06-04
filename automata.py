from abc import ABC, abstractmethod
from automataState import *
from operators import Operators as OP
from utils import *
import copy

# automata base class. Note that this class is abstract
class Automata(ABC):
    @abstractmethod
    def __init__(self, states, initial, final, name):
        if states:
            assert(isinstance(states, list))
            if len(states):
                assert(isinstance(states[0], BaseState))
        
        if initial:
            assert(isinstance(initial, BaseState))

        if final:
            assert(isinstance(final, list))
            if len(final):
                assert(isinstance(final[0], BaseState))

        assert(isinstance(name, str))
        self.name = name
        self.initial = initial
        self.final = final
        self.states = states
        self.deadState = DeterministicState({})

# deterministic finite automata
class DFA(Automata):
    def __init__(self, states, initial, final, name = "DFADefaultName"):
        # parent constructor
        super().__init__(states, initial, final, name)
        isinstance(states, list)
        for state in states:
            assert(isinstance(state, DeterministicState))

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

    # executes one step in the automata
    def __step(self, currentState, char, trace = False):
        try:
            nextState = currentState[char]
        except KeyError:
            nextState = self.__deadState
        if (trace):
            print(f"{currentState} -{char}-> {nextState}")
        return nextState

# non deterministic automata
class NFA(Automata):
    def __init__(self, states, initial, final, name="NFADefaultName"):
        super().__init__(states, initial, final, name)
        isinstance(states, list)
        for state in states:
            assert(isinstance(state, NonDeterministicState))
    
    def toDFA(self):      
        setList = [set([self.initial])]
        newStates = {}

        toProcess = [[self.initial]]
        index = 0
        lenProcess = 1

        while True:
            if index == lenProcess:
                break

            currentStates = toProcess[index]

            states = self.__lambda_closure(currentStates)
            newStateTransitionSymbols = list(set([
                transition for state in states for transition in state.transitions.keys()
            ]))
            newStateTransisions = {symbol : self.__fromStatesBySymbol(states, symbol) for symbol in newStateTransitionSymbols}
            
            for symbol, s in newStateTransisions.items():
                setS = set(s)
                
                if setS not in setList:
                    setList.append(setS)
                    toProcess.append(s)
                    lenProcess += 1
            
            stateIndex = setList.index(set(states))
            if stateIndex not in newStates.keys():
                newStates[stateIndex] = {key : set(newStateTransisions[key]) for key in newStateTransisions.keys()}
            index += 1

        newDeterministicStates = []
        for i in range(len(setList)):
            newState = DeterministicState({})
            newState.label = str(setList[i])
            newDeterministicStates.append(newState)

        for index, transitions in newStates.items():
            state = newDeterministicStates[index]
            for key, value in transitions.items():
                state.addTransition(key, newDeterministicStates[setList.index(value)])
        
        finals = list(filter(lambda x: len(set(self.final).intersection(x)), setList))
        finals = list(map(lambda x: newDeterministicStates[setList.index(x)], finals))

        return DFA(newDeterministicStates, newDeterministicStates[0], finals)

    def __lambda_closure(self, states):
        assert(isinstance(states, list))
        closure = states
        lenClosure = 1
        index = 0
        while 1:
            if index == lenClosure:
                break

            try:
                state = closure[index]
                to_visit = state[OP.EPSILON]
                for i in to_visit:
                    if i not in closure:
                        closure.append(i)
                        lenClosure += 1
            except KeyError:
                pass

            index += 1
        # print(closure)
        return list(set(closure))
        
    def __fromStatesBySymbol(self, states, symbol):
        assert(isinstance(states, list))
        destinyStates = []
        for state in states:
            try:
                for destinyState in state[symbol]:
                    destinyStates.append(destinyState)
            except KeyError:
                pass
        return list(set(destinyStates))


def t1():
    p = NonDeterministicState({})
    q = NonDeterministicState({})
    r = NonDeterministicState({})
    s = NonDeterministicState({})
    p.label = "p"
    q.label = "q"
    r.label = "r"
    s.label = "s"
    p.addTransitions("0", [q, s])
    p.addTransitions("1", [q])
    q.addTransitions("0", [r])
    q.addTransitions("1", [q, r])
    r.addTransitions("0", [s])
    r.addTransitions("1", [p])
    s.addTransitions("1", [p])

    nfa = NFA([p,q,r,s], initial = p, final = [q, s])
    nfa.toDFA()

def t2():
    q0 = NonDeterministicState({})
    q1 = NonDeterministicState({})
    q2 = NonDeterministicState({})
    q3 = NonDeterministicState({})
    q4 = NonDeterministicState({})
    q0.label = "q0"
    q1.label = "q1"
    q2.label = "q2"
    q3.label = "q3"
    q4.label = "q4"
    q0.addTransitions("0", [q1])
    q0.addTransitions("1", [q2])
    q1.addTransitions("0", [q1, q3])
    q1.addTransitions("1", [q1])
    q2.addTransitions("0", [q2])
    q2.addTransitions("1", [q2, q4])

    nfa = NFA([q0,q1,q2,q3,q4], initial = q0, final = [q1, q2])
    return nfa.toDFA()

def t3():
    p = NonDeterministicState({})
    q = NonDeterministicState({})
    r = NonDeterministicState({})
    p.label = "p"
    q.label = "q"
    r.label = "r"
    p.addTransitions("&", [p,q])
    p.addTransitions("b", [q])
    p.addTransitions("c", [r])
    q.addTransitions("a", [p])
    q.addTransitions("b", [r])
    q.addTransitions("c", [p,q])

    nfa = NFA([p,q,r], initial = p, final = [r])
    return nfa.toDFA()

def main():
    t2Var = t3()
    list_of_symbols = list(set([transition for state in t2Var.states for transition in state.transitions.keys()]))  
    automata_to_csv("output/determinizacao2.csv", t2Var, list_of_symbols)

if __name__ == "__main__":
    main()
