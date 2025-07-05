#ifndef LEX_H
#define LEX_H

typedef enum {
    OPEN_PAREN,
    CLOSE_PAREN,
    OPEN_BRACE,
    CLOSE_BRACE,
    COMMA,
    COLON,
    EQUAL,
    PLUS,
    MINUS,
    MUL,
    DIV,
    STRING,
    NUMBER,
    FOR,
    TO,
    WHILE,
    IF,
    ELSE,
    RETURN,
    FUNC,
    VAR,
    ID,
} TokenKind;

typedef struct {
    TokenKind kind;
    const char *text;
} Token;

#endif
