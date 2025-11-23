from enum import Enum 
from token_1 import Token
from token_type import TokenType

# --- 2. The Corrected Lexer Class ---

class Lexer:
    # Constructor: initializes the lexer with the pattern string
    def __init__(self, pattern: str):
        # All members of the class must be indented once inside the def
        self.pattern = pattern
        self.pos = 0
        self.current_char = self.pattern[0] if pattern else None

    # Helper method: advances the position and updates the current character
    # This method must be a peer of __init__
    def advance(self):
        self.pos += 1
        
        # Logic to update current_char
        if self.pos < len(self.pattern):
            self.current_char = self.pattern[self.pos]
        else:
            # Correctly aligned else for end of input
            self.current_char = None 

    # Main method: returns the next token from the pattern
    # This method must be a peer of __init__ and advance
    def get_next_token(self) -> Token:
        # Loop to consume whitespace characters
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
                continue

            # Token recognition based on the character
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')
            elif self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')
            elif self.current_char == '|':
                self.advance()
                return Token(TokenType.OR, '|')
            elif self.current_char == '*':
                self.advance()
                return Token(TokenType.STAR, '*')
            elif self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')
            elif self.current_char == '?':
                self.advance()
                return Token(TokenType.OPTIONAL, '?')
            elif self.current_char == 'ε':
                self.advance()                
                return Token(TokenType.EPSILON, 'ε')
            elif self.current_char.isdigit():
                digit = self.current_char
                self.advance()
                return Token(TokenType.DIGIT, digit)
            else:
                char = self.current_char
                self.advance()
                return Token(TokenType.CHAR, char)
        
        # NOTE: Your original logic had an isdigit() check but returned 'char'.
        # Assuming any character not matched above is a literal character.
        # The isdigit() check is redundant if CHAR is the catch-all.
        # Returning Token(TokenType.CHAR, char) is the correct catch-all.
        return Token(TokenType.END)
        
# --- 3. Lexer Test Function (Corrected Indentation) ---

def test_lexer():
    print("Testing Lexer...")
    
    # Using the example pattern from your original test block
    pattern_string = "a+1? (c|d)* ε"
    print(f"Input Pattern: '{pattern_string}'")

    lexer = Lexer(pattern_string)
    tokens = []
    
    # Loop to continuously get tokens until the END token is reached
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.END:
            break
            
    print("\nTokens Generated:")
    for token in tokens:
        print(f"  {token}")


if __name__ == "__main__":
    test_lexer()