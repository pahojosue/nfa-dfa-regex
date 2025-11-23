import re 
from enum import Enum 
from typing import List, Optional, Set

class ASTNode:
    pass

class CharNode(ASTNode):
    def __init__(self, char: str):
        self.char = char
    
    def __repr__(self):
        return f"Char('{self.char}')"

class DigitNode(ASTNode):
    def __init__(self, digit: str):
        self.digit = digit
    
    def __repr__(self):
        return f"Digit('{self.digit}')"

class StarNode(ASTNode):
    def __init__(self, expr: ASTNode):
        self.expr = expr
    
    def __repr__(self):
        return f"Star({self.expr})"

class PlusNode(ASTNode):
    def __init__(self, expr: ASTNode):
        self.expr = expr
    
    def __repr__(self):
        return f"Plus({self.expr})"

class OptionalNode(ASTNode):
    def __init__(self, expr: ASTNode):
        self.expr = expr
    
    def __repr__(self):
        return f"Optional({self.expr})"

class OrNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"Or({self.left}, {self.right})"

class ConcatNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"Concat({self.left}, {self.right})"