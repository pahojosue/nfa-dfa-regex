from enum import Enum

class TokenType(Enum):
    CHAR = 1
    DIGIT = 2
    STAR = 3
    PLUS = 4
    OPTIONAL = 5
    OR = 6
    LPAREN = 7
    RPAREN = 8
    EPSILON = 9
    END = 10

