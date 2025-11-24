import graphviz
from lexer import Lexer, test_lexer
from regex_parser import Parser, test_parser
from nfa import NFA
from state import State
from nfa_builder import NFABuilder, test_nfa_builder
from pathlib import Path
import glob
from collections import deque

class RegexToNFAConverter:
    def __init__(self):
        self.nfa = None
    
    def convert(self, regex: str) -> NFA:
        """
        Build an NFA from regex. Reset State id counter so new NFA starts at q0.
        """
        State.reset_id_counter()
        lexer = Lexer(regex)
        parser = Parser(lexer)
        ast = parser.parse()
        self.nfa = NFABuilder.build_from_ast(ast)
        return self.nfa
    
    def add_explicit_concatenation(self, regex: str) -> str:
        # keep current behavior (no-op) unless you want to insert explicit concat ops
        return regex
    
    def visualize(self):
        """Convenience: render to default filename nfa_thompson"""
        self.visualize_with_graphviz("nfa_thompson")
    
    def visualize_with_graphviz(self, filename: str = "nfa_thompson"):
        """
        Render the current NFA with Graphviz. States are labeled q0..qN in BFS order
        starting from the start state. Old files with the same basename are removed
        before rendering.
        """
        if not self.nfa:
            print("No NFA to visualize. Convert a regex first.")
            return

        # Remove previous files with same base name (png, svg, gv, etc.)
        base = Path(filename)
        pattern = str(base.with_suffix("") ) + ".*"
        for old in glob.glob(pattern):
            try:
                Path(old).unlink()
            except Exception:
                pass

        # Collect states by BFS from start to ensure q0 is the start and numbering is consecutive
        start = self.nfa.start
        visited = []
        seen = set()
        q = deque([start])
        seen.add(start)
        while q:
            s = q.popleft()
            visited.append(s)
            # enqueue epsilon and normal transitions
            for nxt in s.epsilon_transitions:
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
            for dests in s.transitions.values():
                for nxt in dests:
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append(nxt)

        # Map each state to sequential label index: q0, q1, ...
        state_index = {s: idx for idx, s in enumerate(visited)}

        # Build Graphviz graph
        dot = graphviz.Digraph(comment='NFA Thompson Construction')
        dot.attr(rankdir='LR', size='8,5')

        # Invisible start arrow to q0
        dot.node('start', shape='point')
        dot.edge('start', f"q{state_index[self.nfa.start]}", label='')

        # Nodes with accept doublecircle
        for s, idx in state_index.items():
            shape = 'doublecircle' if s.is_accept else 'circle'
            dot.node(f"q{idx}", label=f"q{idx}", shape=shape)

        # Edges: transitions and epsilons
        for s in visited:
            src = f"q{state_index[s]}"
            # normal transitions
            for ch, dests in s.transitions.items():
                for d in dests:
                    dst = f"q{state_index[d]}"
                    dot.edge(src, dst, label=str(ch))
            # epsilon transitions
            for d in s.epsilon_transitions:
                dst = f"q{state_index[d]}"
                dot.edge(src, dst, label='ε')

        # Render and cleanup intermediate files
        out = dot.render(filename, format='png', cleanup=True)
        print(f"📊 NFA Thompson visualization saved as: {out}")
        
        # Also display in the console
        print("Graphviz NFA Structure:")
        print(dot.source)
        
        return dot

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

# if __name__ == "__main__":
#     # test_lexer()
#     # test_parser()
#     test_nfa_builder()
#     test_converter()

def interactive_demo():
    """Interactive demo for testing custom regex patterns with Graphviz"""
    converter = RegexToNFAConverter()

    print("\n" + "="*60)
    print("INTERACTIVE REGEX TO NFA CONVERTER WITH GRAPHVIZ")
    print("="*60)
    print("Supported features: ")
    print("  - Letters: a, b, c, ...")
    print("  - Digits: 0, 1, 2, ...")
    print("  - Operators: * + ? | ( )")
    print("  - Epsilon: ε")
    print("Commands: ")
    print("  - 'visualize' - Generate Graphviz diagram")
    print("  - 'text' - Show text visualization") 
    print("  - 'back' - New regex")
    print("  - 'quit' - Exit")
    print("="*60)

    while True:
        try:
            regex = input("\nEnter regex: ").strip()
            if regex.lower() == 'quit':
                break

            if not regex:
                continue

            # Convert
            nfa = converter.convert(regex)
            print(f"\n✅ Successfully converted '{regex}' to NFA")

            # Test strings interactively
            while True:
                command = input("\nEnter test string or command: ").strip()
                
                if command.lower() == 'back':
                    break
                if command.lower() == 'quit':
                    return
                if command.lower() == 'visualize':
                    # Generate Graphviz visualization
                    filename = f"nfa_{regex.replace('|', '_or_').replace('*', '_star').replace('+', '_plus').replace('?', '_optional').replace('(', '_').replace(')', '_')}"
                    converter.visualize_with_graphviz(filename)
                    continue
                if command.lower() == 'text':
                    # Show text visualization
                    converter.visualize()
                    continue
                
                # Otherwise, treat as test string
                result = nfa.simulate(command)
                print(f"  '{command}' -> {'✅ ACCEPT' if result else '❌ REJECT'}")
                
        except Exception as e:
            print(f"Error: {e}")

def demo_thompson_patterns():
    """Demo common regex patterns to show Thompson's construction"""
    converter = RegexToNFAConverter()
    
    patterns = [
        ("a", "Single character"),
        ("a*", "Kleene star"),
        ("a+", "One or more (Plus)"),
        ("a?", "Optional"),
        ("a|b", "Alternation"),
        ("ab", "Concatenation"),
        ("a(b|c)", "Complex pattern"),
    ]
    
    print("\n" + "="*60)
    print("THOMPSON'S CONSTRUCTION DEMO")
    print("="*60)
    
    for pattern, description in patterns:
        print(f"\n📋 Pattern: {pattern} ({description})")
        try:
            nfa = converter.convert(pattern)
            
            # Test a few strings
            test_cases = {
                "a": ["a"],
                "a*": ["", "a", "aa"],
                "a+": ["a", "aa"],
                "a?": ["", "a"],
                "a|b": ["a", "b"],
                "ab": ["ab"],
                "a(b|c)": ["ab", "ac"]
            }
            
            if pattern in test_cases:
                for test_str in test_cases[pattern]:
                    result = nfa.simulate(test_str)
                    print(f"  '{test_str}' -> {'✅' if result else '❌'}")
            
            # Generate visualization
            filename = f"thompson_{pattern.replace('|', '_or_').replace('*', '_star')}"
            converter.visualize_with_graphviz(filename)
            
        except Exception as e:
            print(f"  Error: {e}")

def main():
    """Main function to run the complete system"""
    print("🔤 Regex to NFA Converter using Thompson's Construction")
    print("Now with: digits [0-9], + (one or more), ? (optional)")
    print("         Graphviz visualization in Thompson's style")

    # Ask user what they want to do
    choice = input("\nChoose mode:\n1. Interactive demo\n2. Thompson patterns demo\n3. Run tests\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        interactive_demo()
    elif choice == '2':
        demo_thompson_patterns()
    elif choice == '3':
        test_lexer()
        test_parser("a+1? (c|d)* ε")
        test_nfa_builder()
        test_converter()
    else:
        interactive_demo()

if __name__ == "__main__":
    main()