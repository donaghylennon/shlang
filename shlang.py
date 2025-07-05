#!/usr/bin/env python
import lexer
import parser
from pprint import pprint

prog = """
func main(): int {
    var x: int
    var y: string
    if x {
        thing()
    } else {
    }
    for i : int = 1 to 10 {
        x = what(y)
    }
}

func what(y: string) {
    return toint(y)
}
"""

def main():
    l = lexer.Lexer(prog)
    out = l.lex()

    p = parser.Parser(out)
    ast = p.parse()
    parser.print_ast(ast)

if __name__ == "__main__":
    main()
