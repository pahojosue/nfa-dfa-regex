from lexer import Lexer, test_lexer
from regex_parser import Parser, test_parser
from nfa import NFA
from nfa_builder import NFABuilder, test_nfa_builder

class RegexToNFAConverter:
    def __init__(self):
        self.nfa = None
    
    def convert(self, regex: str) -> NFA:
        # Add explicit concatenation operators
        regex = self.add_explicit_concatenation(regex)
        lexer = Lexer(regex)
        parser = Parser(lexer)
        ast = parser.parse()

        self.nfa = NFABuilder.build_from_ast(ast)
        return self.nfa
    
    def add_explicit_concatenation(self, regex: str) -> str:
        """Add '.' for explicit concatenation"""
        if not regex:
            return regex
        
        result = []
        for i in range(len(regex) - 1):
            result.append(regex[i])
            current = regex[i]
            next_char = regex[i+1]

            #Conditions where we need to add concatenation
            if ((current not in ['(', '|'] and next_char not in ['|', '*', '+', '?', ')']) or (current == ')' and next_char not in ['|', '*', '+', '?', ')']) or (current in ['*', '+', '?'] and next_char not in ['|', '*', '+', '?'])):
                result.append('.')
                result.append(regex[-1])
                return ''.join(result)
    
    def visualize(self):
        """Simple text-based visualization"""
        if not self.nfa:
            return
        
        visited = set()

        def dfs(state, depth=0):
            if state in visited:
                return
            visited.add(state)

            indent = "  " * depth
            status = " (accept)" if state.is_accept else ""
            print(f"{indent}{state}{status}")

            # Character transitions
            for char, next_states in state.transitions.items():
                for next_state in next_states:
                    print(f"{indent} --'{char}'--> {next_state}")
                    dfs(next_state, depth + 1)
            
            # Epsilon transitions
            for next_state in state.epsilon_transitions:
                print(f"{indent} --ε--> {next_state}")
                dfs(next_state, depth + 1)
        
        print("NFA Structure: ")
        dfs(self.nfa.start)

# Test the complete converter
def test_converter():
    print("\nTesting Complete Converter...")
    converter = RegexToNFAConverter()
    nfa = converter.convert("a+1?")
    print("NFA Simulation tests: ")
    test_strings = ["a1", "aa1", "a", "1", "aa", "aaa1"]
    for test_str in test_strings:
        result = nfa.simulate(test_str)
        print(f"  '{test_str}' -> {result}")
    
    print("\nNFA Visualization: ")
    converter.visualize()

if __name__ == "__main__":
    test_lexer()
    # test_parser()
    test_nfa_builder()
    test_converter()

def interactive_demo():
    """Interactive demo for testing custom regex patterns"""
    converter = RegexToNFAConverter()

    print("\n" + "="*60)
    print("INTERACTIVE REGEX TO NFA CONVERTER")
    print("="*60)
    print("Supported features: ")
    print("  - Letters: a, b, c, ...")
    print("  - Digits: 0, 1, 2, ...")
    print("  - Operators: * + ? | ( )")
    print("  - Epsilon: ε")
    print("Type 'quit' to exit")
    print("="*60)

    while True:
        try:
            regex = input("\nEnter regex: ").strip()
            if regex.lower() == 'quit':
                break

            if not regex:
                continue

            # Convert and visualize
            nfa = converter.convert(regex)
            print(f"\n Successfully converted '{regex}' to NFA")

            # Test strings interactively
            while True:
                test_str = input("\nEnter test string ( or 'back' for new regex, 'quit' to exit): ").strip()
                if test_str.lower() == 'back':
                    break
                if test_str.lower() == 'quit':
                    return
                
                result = nfa.simulate(test_str)
                print(f"  '{test_str}' -> {'✔ ACCEPT' if result else '✖ REJECT'}")
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main function to run the complete system"""
    print("Regex to NFA Converter")
    print("Now with: digits [0-9], + (one or more), ? (optional)")

    # Start interactive demo
    interactive_demo()

if __name__ == "__main__":
    main()