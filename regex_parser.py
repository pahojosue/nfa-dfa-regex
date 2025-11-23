from lexer import Lexer
from ast_nodes import ASTNode, CharNode, DigitNode, StarNode, OptionalNode, PlusNode, ConcatNode, OrNode
from token_type import TokenType

# Tokens that can START a new expression or sub-expression (Literal or Group)
_PRIMARY_STARTERS = [TokenType.CHAR, TokenType.DIGIT, TokenType.EPSILON, TokenType.LPAREN]

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    
    def eat(self, token_type: TokenType):
        """Consumes the current token if it matches the expected type and advances."""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(f"Expected {token_type.name}, got {self.current_token.type.name} at position {self.lexer.pos}")
    
    
    def factor(self) -> ASTNode:
        """
        Handles the smallest unit: a single literal or a parenthesized expression.
        Production: factor -> CHAR | DIGIT | EPSILON | ( expr )
        """
        token = self.current_token
        
        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        
        elif token.type == TokenType.CHAR: 
            self.eat(TokenType.CHAR)
            return CharNode(token.value)
        
        elif token.type == TokenType.DIGIT:
            self.eat(TokenType.DIGIT)
            return DigitNode(token.value)
        
        elif token.type == TokenType.EPSILON:
            self.eat(TokenType.EPSILON)
            return CharNode('ε')
        
        else:
            raise SyntaxError(f"Unexpected token in factor: {token}")
    
    
    def term(self) -> ASTNode:
        """
        Handles the unary/postfix operators: *, +, ?. (Highest Precedence)
        Production: term -> factor { * | + | ? }
        """
        node = self.factor()
        
        while self.current_token.type in [TokenType.STAR, TokenType.PLUS, TokenType.OPTIONAL]:
            if self.current_token.type == TokenType.STAR:
                self.eat(TokenType.STAR)
                node = StarNode(node)
            elif self.current_token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                node = PlusNode(node)
            elif self.current_token.type == TokenType.OPTIONAL: 
                self.eat(TokenType.OPTIONAL)
                node = OptionalNode(node)
        
        return node
    
    
    def concat(self) -> ASTNode:
        """
        Handles implicit concatenation. (Medium Precedence)
        Production: concat -> term { term }
        """
        node = self.term()
        
        # Implicit concatenation occurs when the current token is one that can
        # legally start a new expression immediately after the previous one.
        while (self.current_token.type in _PRIMARY_STARTERS):
            right = self.term()
            node = ConcatNode(node, right)
        
        return node
    
    
    def expr(self) -> ASTNode:
        """
        Handles the OR operator: |. (Lowest Precedence)
        Production: expr -> concat { | concat }
        """
        node = self.concat()
        
        while self.current_token.type == TokenType.OR:
            self.eat(TokenType.OR)
            right = self.concat()
            node = OrNode(node, right)
        
        return node 
    
    
    def parse(self) -> ASTNode:
        """Entry point for the parser."""
        ast = self.expr()
        self.eat(TokenType.END) # Ensure we've consumed all input
        return ast

# Test the parser
def test_parser(pattern: str):
    print("\nTesting Parser...")
    
    lexer = Lexer(pattern)
    parser = Parser(lexer)
    
    try:
        ast = parser.parse()
        print(f"Input: '{pattern}'")
        print("AST:", ast)
    except SyntaxError as e:
        print(f"Input: '{pattern}'")
        print(f"Parsing Error: {e}")

if __name__ == "_main_":
    # Ensure Lexer is tested first to provide context for the tokens
    
    # 1. Your original example
    # Expected: Concat(Plus(Char('a')), Optional(Digit('1')))
    # The 'a' and '1' are concatenated implicitly.
    test_parser("a+1?") 

    # 2. Grouping
    # Expected: Star(Or(Char('a'), Char('b')))
    test_parser("(a|b)*")
    
    # 3. Concatenation and Or Precedence
    # Expected: Or(Concat(Char('a'), Char('b')), Char('c'))
    test_parser("ab|c")