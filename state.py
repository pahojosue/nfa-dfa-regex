import re 
from enum import Enum 
from typing import List, Optional, Set, Dict


class State:
    _id_counter = 0
    
    def __init__(self, is_accept: bool = False):
        self.id = State._id_counter
        State._id_counter += 1
        self.is_accept = is_accept
        self.transitions: Dict[str, Set["State"]] = {}  # char -> set of states
        self.epsilon_transitions: Set["State"] = set()
    
    def add_transition(self, char: str, state: "State"):
        if char not in self.transitions:
            self.transitions[char] = set()
        self.transitions[char].add(state)
    
    def add_epsilon_transition(self, state: "State"):
        self.epsilon_transitions.add(state)
    
    def __repr__(self):
        return f"State({self.id}, accept={self.is_accept})"