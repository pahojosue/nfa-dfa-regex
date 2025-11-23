from typing import Set
from state import State

class NFA:
    def __init__(self, start: State, accept: State):
        self.start = start
        self.accept = accept
    
    def get_epsilon_closure(self, states: Set[State]) -> Set[State]:
        """Get all states reachable via epsilon transitions"""
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            for next_state in state.epsilon_transitions:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure
    
    def simulate(self, input_string: str) -> bool:
        """Simulate NFA on input string"""
        current_states = self.get_epsilon_closure({self.start})

        for char in input_string:
            next_states: Set[State] = set()
            for state in current_states:
                if char in state.transitions:
                    next_states.update(state.transitions[char])

            current_states = self.get_epsilon_closure(next_states)
            if not current_states:
                return False

        return any(state.is_accept for state in current_states)