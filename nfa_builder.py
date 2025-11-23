from nfa import NFA
from state import State
from lexer import Lexer
from regex_parser import Parser
from ast_nodes import CharNode, DigitNode, StarNode, PlusNode, OptionalNode, OrNode, ConcatNode
from ast_nodes import ASTNode

class NFABuilder:
    @staticmethod
    def build_from_ast(node: ASTNode) -> NFA:
        if isinstance(node, CharNode):
            return NFABuilder.build_char(node.char)
        elif isinstance(node, DigitNode):
            return NFABuilder.build_digit(node.digit)
        elif isinstance(node, StarNode):
            return NFABuilder.build_star(NFABuilder.build_from_ast(node.expr))
        elif isinstance(node, PlusNode):
            return NFABuilder.build_plus(NFABuilder.build_from_ast(node.expr))
        elif isinstance(node, OptionalNode):
            return NFABuilder.build_optional(NFABuilder.build_from_ast(node.expr))
        elif isinstance(node, OrNode):
            left_nfa = NFABuilder.build_from_ast(node.left)
            right_nfa = NFABuilder.build_from_ast(node.right)
            return NFABuilder.build_or(left_nfa, right_nfa)
        elif isinstance(node, ConcatNode):
            left_nfa = NFABuilder.build_from_ast(node.left)
            right_nfa = NFABuilder.build_from_ast(node.right)
            return NFABuilder.build_concat(left_nfa, right_nfa)
    
    @staticmethod
    def build_char(char: str) -> NFA:
        start = State()
        accept = State(is_accept = True)
        start.add_transition(char, accept)
        return NFA(start, accept)
    
    @staticmethod
    def build_digit(digit: str) -> NFA:
        start = State()
        accept = State(is_accept = True)
        start.add_transition(digit, accept)
        return NFA(start, accept)
    
    @staticmethod
    def build_star(nfa: NFA) -> NFA:
        """a* : zero or more occurences"""
        start = State()
        accept = State(is_accept = True)

        # ε: start -> nfa.start
        start.add_epsilon_transition(nfa.start)
        # ε: start -> accept
        start.add_epsilon_transition(accept)
        # ε: nfa.accept -> nfa.start
        nfa.accept.add_epsilon_transition(nfa.start)
        # ε: nfa.accept -> accept
        nfa.accept.add_epsilon_transition(accept)
        nfa.accept.is_accept = False

        return NFA(start, accept)
    
    @staticmethod
    def build_plus(nfa: NFA) -> NFA:
        """a+ : one or more occurences"""
        start = State()
        accept = State(is_accept = True)

        # ε: start -> nfa.start
        start.add_epsilon_transition(nfa.start)
        # ε: nfa.accept -> nfa.start (loop back)
        nfa.accept.add_epsilon_transition(nfa.start)
        # ε: nfa.accept -> accept
        nfa.accept.add_epsilon_transition(accept)
        nfa.accept.is_accept = False

        return NFA(start, accept)
    
    @staticmethod
    def build_optional(nfa: NFA) -> NFA:
        """a? : zero or one occurence"""
        start = State()
        accept = State(is_accept = True)

        # ε: start -> nfa.start
        start.add_epsilon_transition(nfa.start)
        # ε: start -> accept (skip the expression)
        start.add_epsilon_transition(accept)
        # ε: nfa.accept -> nfa.start
        nfa.accept.add_epsilon_transition(nfa.start)
        # ε: nfa.accept -> accept
        nfa.accept.add_epsilon_transition(accept)
        nfa.accept.is_accept = False

        return NFA(start, accept)
    
    @staticmethod
    def build_or(nfa1: NFA, nfa2: NFA) -> NFA:
        start = State()
        accept = State(is_accept = True)

        # ε: start -> nfa1.start
        start.add_epsilon_transition(nfa1.start)
        # ε: start -> nfa2.start
        start.add_epsilon_transition(nfa2.start)
        # ε: nfa1.accept -> accept
        nfa1.accept.add_epsilon_transition(accept)
        # ε: nfa2.accept -> accept
        nfa2.accept.add_epsilon_transition(accept)

        nfa1.accept.is_accept = False
        nfa2.accept.is_accept = False

        return NFA(start, accept)
    
    @staticmethod 
    def build_concat(nfa1: NFA, nfa2: NFA) -> NFA: 
        # ε: nfa1.accept → nfa2.start 
        nfa1.accept.add_epsilon_transition(nfa2.start) 
        nfa1.accept.is_accept = False 
         
        return NFA(nfa1.start, nfa2.accept) 
    
# Test the NFA builder
def test_nfa_builder():
    print("\nTesting NFA Builder...")
    lexer = Lexer("a")
    parser = Parser(lexer)
    ast = parser.parse()
    nfa = NFABuilder.build_from_ast(ast)
    print("NFA Created: ", nfa)
    print("Start state: ", nfa.start)
    print("Accept state: ", nfa.accept)

# if __name__ == "__main__":
#     test_lexer()
#     test_parser()
#     test_nfa_builder()