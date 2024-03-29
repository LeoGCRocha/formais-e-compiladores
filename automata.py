from abc import ABC, abstractmethod
from operators import Operators as OP
from copy import deepcopy
from automataState import *
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

    def listOfSymbols(self):
        return list(set([transition for state in self.states for transition in state.transitions.keys()]))
    
    def statesLabelToId(self):
        for state in self.states:
            state.label = state.id

    def __add__(self, other):
        assert(isinstance(other, Automata))
        automata1 = deepcopy(self)
        automata2 = deepcopy(other)
        # add new initial statess
        new_initial_state = NonDeterministicState({})
        new_initial_state.label = automata1.initial.label + automata2.initial.label
        new_final_state = NonDeterministicState({})
        new_final_state.label = "final"
        new_initial_state.addTransition(OP.EPSILON, automata1.initial)
        new_initial_state.addTransition(OP.EPSILON, automata2.initial)
        # add new final state
        for state in automata1.final:
            state.addTransition(OP.EPSILON, new_final_state)
        for state in automata2.final:
            state.addTransition(OP.EPSILON, new_final_state)
        automata = NFA([new_initial_state]+automata1.states+automata2.states+[new_final_state], new_initial_state, [new_final_state], "Union Automata")
        # Determinization
        return automata

# deterministic finite automata
class DFA(Automata):
    def __init__(self, states, initial, final, name = "DFADefaultName"):
        # parent constructor
        super().__init__(states, initial, final, name)
        isinstance(states, list)
        for state in states:
            assert(isinstance(state, DeterministicState))

    def clean(self):
        for state in self.states:
            state.transitions.pop(OP.EPSILON, None)
        self.statesLabelToId()

    # run the automata, given the input
    def run(self, text, trace = False):
        lexemes = []
        splittedText = text.split()
        for string in splittedText:
            # print(string)
            lastIndexChar = 0
            currentState = copy.deepcopy(self.initial)
            indexChar = 0
            while indexChar < len(string):
            # for indexChar in range(0, len(string)):
                nextState = self.__step(currentState, string[indexChar], trace)
                if (nextState == self.deadState):
                    if (currentState.id == self.initial.id):
                        raise(Exception(f"caracter na posicao {indexChar} em \"{string}\" não encaixa o lexema em algum padrão"))
                    lexemes.append([string[lastIndexChar:indexChar], currentState])
                    lastIndexChar = indexChar
                    currentState = copy.deepcopy(self.initial)
                else:
                    currentState = nextState
                    indexChar += 1
                lastState = currentState

            if lastState != self.deadState:
                lexemes.append([string[lastIndexChar:], lastState])
            
        return lexemes

    # executes one step in the automata
    def __step(self, currentState, char, trace = False):
        try:
            nextState = currentState[char]
        except KeyError:
            nextState = self.deadState
        if (trace):
            print(f"{currentState} -{char}-> {nextState}")
        return nextState

    def toNFA(self):
        new_states = []
        final_states = []
        # Define list of new states
        for state in self.states:
            stateNonDeterministic = NonDeterministicState({})
            stateNonDeterministic.label = state.label
            new_states.append(stateNonDeterministic)
        # Define initial state
        initialState = new_states[self.states.index(self.initial)]
        for position in range (0, len(self.states)):
            for key,value in self.states[position].transitions.items():
                new_states[position].addTransition(key, new_states[self.states.index(value)])
        # Define final states
        for state in self.final:
            final_states.append(new_states[self.states.index(state)])
        return NFA(new_states, initialState, final_states, "NFA from DFA")
        
# non deterministic automata
class NFA(Automata):
    def __init__(self, states, initial, final, name="NFADefaultName"):
        super().__init__(states, initial, final, name)
        isinstance(states, list)
        for state in states:
            assert(isinstance(state, NonDeterministicState))
    
    def toDFA(self):
        newInitial = self.__lambda_closure([self.initial])
        setList = [set(newInitial)]
        newStates = {}

        toProcess = [newInitial]
        index = 0
        lenProcess = 1

        while True:
            if index == lenProcess:
                break

            currentStates = toProcess[index]
            # states = self.__lambda_closure(currentStates)
            states = currentStates

            newStateTransitionSymbols = list(set([
                transition for state in states for transition in state.transitions.keys()
            ]))
            try:
                newStateTransitionSymbols.remove(OP.EPSILON)
            except ValueError:
                pass

            newStateTransitions = {symbol : self.__lambda_closure(self.__fromStatesBySymbol(states, symbol)) for symbol in newStateTransitionSymbols}

            for symbol, s in newStateTransitions.items():
                setS = set(s)

                if setS not in setList:
                    setList.append(setS)
                    toProcess.append(s)
                    lenProcess += 1
            
            stateIndex = setList.index(set(states))
            if stateIndex not in newStates.keys():
                newStates[stateIndex] = {key : set(newStateTransitions[key]) for key in newStateTransitions.keys()}
            index += 1

        newDeterministicStates = []
        for i in range(len(setList)):
            newState = DeterministicState({})
            newState.label = str(setList[i])
            newDeterministicStates.append(newState)
            newState.meaning = list(map(lambda x: x[0], list(filter([].__ne__, list(map(lambda x: x.meaning, setList[i]))))))

        for index, transitions in newStates.items():
            state = newDeterministicStates[index]
            for key, value in transitions.items():
                state.addTransition(key, newDeterministicStates[setList.index(value)])

        finals = list(filter(lambda x: len(set(self.final).intersection(x)), setList))
        finals = list(map(lambda x: newDeterministicStates[setList.index(x)], finals))

        dfa = DFA(newDeterministicStates, newDeterministicStates[0], finals)
        dfa.clean()
        return dfa

    def __lambda_closure(self, states):
        assert(isinstance(states, list))
        closure = states
        lenClosure = len(closure)
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
    return nfa.toDFA()

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
    s1 = NonDeterministicState({})
    s2 = NonDeterministicState({})
    s3 = NonDeterministicState({})
    s4 = NonDeterministicState({})
    s5 = NonDeterministicState({})
    s6 = NonDeterministicState({})
    s7 = NonDeterministicState({})
    s1.label = "1"
    s2.label = "2"
    s3.label = "3"
    s4.label = "4"
    s5.label = "5"
    s6.label = "6"
    s7.label = "7"
    s1.addTransitions(OP.EPSILON, [s2, s6])
    s2.addTransitions("i", [s3])
    s3.addTransitions("f", [s4])
    s4.addTransitions(OP.EPSILON, [s5])
    s6.addTransitions("i", [s7])
    s7.addTransitions(OP.EPSILON, [s5])
    nfa = NFA([s1,s2,s3,s4,s5,s6,s7], initial = s1, final = [s5])
    return nfa.toDFA()

def t4():
    # first automata : aa
    p = NonDeterministicState({})
    q = NonDeterministicState({})
    r = NonDeterministicState({})
    p.label = "1a"
    q.label = "2a"
    r.label = "afinal"
    p.addTransitions("a", [q])
    q.addTransitions("a", [r])
    nfa = NFA([p,q,r], initial = p, final = [r])
    # second automata : bb
    x = NonDeterministicState({})
    y = NonDeterministicState({})
    z = NonDeterministicState({})
    x.label = "1b"
    y.label = "2b"
    z.label = "bfinal"
    x.addTransitions("b", [y])
    y.addTransitions("b", [z])
    nfa2 = NFA([x,y,z], initial = x, final = [z])
    # union by & closure
    nfa3 = nfa + nfa2
    # determinization
    return nfa3.toDFA()