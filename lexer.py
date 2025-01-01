from enum import Enum, auto
import re

class TokenKind(Enum):
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    OPEN_BRACE = auto()
    CLOSE_BRACE = auto()
    COMMA = auto()
    COLON = auto()
    EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    STRING = auto()
    NUMBER = auto()
    FOR = auto()
    TO = auto()
    WHILE = auto()
    IF = auto()
    ELSE = auto()
    RETURN = auto()
    FUNC = auto()
    VAR = auto()
    ID = auto()

class Token:
    def __init__(self, kind, text):
        self.kind = kind
        self.text = text
    
    def __repr__(self):
        return f"Token({self.kind},{self.text})"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.token_start = 0
        self.token_end = 0
        self.ch = self.source[self.pos]

    def next(self):
        self.pos += 1
        if self.pos < len(self.source):
            return self.source[self.pos]
        else:
            return ""

    def peek(self):
        if self.pos + 1 < len(self.source):
            return self.source[self.pos + 1]
        else:
            return ""

    def match(self, item):
        for i, ch in enumerate(item):
            if self.source[self.pos + i] != ch:
                return False
        if not self.source[self.pos + i + 1].isspace():
            return False
        self.pos += i
        self.token_end = self.pos + 1
        return True

    def lex(self):
        tokens = []
        while self.pos < len(self.source):
            self.token_start = self.pos
            self.token_end = self.pos + 1
            match self.ch:
                case " " | "\n" | "\t":
                    pass
                case "(":
                    tokens.append(Token(TokenKind.OPEN_PAREN, self.ch))
                case ")":
                    tokens.append(Token(TokenKind.CLOSE_PAREN, self.ch))
                case "{":
                    tokens.append(Token(TokenKind.OPEN_BRACE, self.ch))
                case "}":
                    tokens.append(Token(TokenKind.CLOSE_BRACE, self.ch))
                case ",":
                    tokens.append(Token(TokenKind.COMMA, self.ch))
                case ":":
                    tokens.append(Token(TokenKind.COLON, self.ch))
                case "=":
                    tokens.append(Token(TokenKind.EQUAL, self.ch))
                case "+":
                    tokens.append(Token(TokenKind.PLUS, self.ch))
                case "-":
                    tokens.append(Token(TokenKind.MINUS, self.ch))
                case "*":
                    tokens.append(Token(TokenKind.MUL, self.ch))
                case "/":
                    tokens.append(Token(TokenKind.DIV, self.ch))
                case '"':
                    self.token_start += 1
                    while self.peek() != '"':
                        self.next()
                        self.token_end += 1
                    self.next()
                    tokens.append(Token(TokenKind.STRING, self.source[self.token_start : self.token_end]))
                case self.ch if re.match("[0-9]", self.ch):
                    while self.peek().isnumeric():
                        self.next()
                        self.token_end += 1
                    tokens.append(Token(TokenKind.NUMBER, self.source[self.token_start : self.token_end]))
                case self.ch if re.match("[a-zA-z_]", self.ch):
                    if self.match("for"):
                        tokens.append(Token(TokenKind.FOR, self.source[self.token_start : self.token_end]))
                    elif self.match("to"):
                        tokens.append(Token(TokenKind.TO, self.source[self.token_start : self.token_end]))
                    elif self.match("while"):
                        tokens.append(Token(TokenKind.WHILE, self.source[self.token_start : self.token_end]))
                    elif self.match("if"):
                        tokens.append(Token(TokenKind.IF, self.source[self.token_start : self.token_end]))
                    elif self.match("else"):
                        tokens.append(Token(TokenKind.ELSE, self.source[self.token_start : self.token_end]))
                    elif self.match("return"):
                        tokens.append(Token(TokenKind.RETURN, self.source[self.token_start : self.token_end]))
                    elif self.match("func"):
                        tokens.append(Token(TokenKind.FUNC, self.source[self.token_start : self.token_end]))
                    elif self.match("var"):
                        tokens.append(Token(TokenKind.VAR, self.source[self.token_start : self.token_end]))
                    else:
                        while re.match("[a-zA-z0-9_]", self.peek()):
                            self.next()
                            self.token_end += 1
                        tokens.append(Token(TokenKind.ID, self.source[self.token_start : self.token_end]))
            self.ch = self.next()
        return tokens
