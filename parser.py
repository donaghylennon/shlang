from lexer import Token, TokenKind

class Program:
    def __init__(self, functions):
        self.functions = functions

    def __repr__(self):
        return f"Program({self.functions})"

class Function:
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body

    def __repr__(self):
        return f"Function({self.name},{self.params},{self.return_type},{self.body})"

class Identifier:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

class Declaration:
    def __init__(self, name, var_type):
        self.name = name
        self.var_type = var_type

    def __repr__(self):
        return f"Declaration({self.name},{self.var_type})"

class CompoundStatement:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"CompoundStatement({self.statements})"

class Assignment:
    def __init__(self, target, value):
        self.target = target
        self.value = value

    def __repr__(self):
        return f"Assignment({self.target},{self.value})"

class If:
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __repr__(self):
        return f"If({self.condition},{self.true_branch},{self.false_branch})"

class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"While({self.condition},{self.body})"

class For:
    def __init__(self, declaration, initial_value, limit, body):
        self.declaration = declaration
        self.initial_value = initial_value
        self.limit = limit
        self.body = body

    def __repr__(self):
        return f"For({self.declaration},{self.initial_value},{self.limit},{self.body})"

class FunctionCall:
    def __init__(self, identifier, args):
        self.identifier = identifier
        self.args = args

    def __repr__(self):
        return f"FunctionCall({self.identifier},{self.args})"

class Return:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"

def print_ast(ast, lvl=0):
    ind = lvl * ' '
    match ast:
        case Program():
            print(f"{ind}Program:")
            for f in ast.functions:
                print_ast(f,lvl+1)
        case Function():
            print(f"{ind}Function:")
            print_ast(ast.name,lvl+1)
            if ast.params:
                for p in ast.params:
                    print_ast(p,lvl+1)
            print_ast(ast.return_type,lvl+1)
            print_ast(ast.body,lvl+1)
        case Identifier():
            print(f"{ind}Identifier:")
            print_ast(ast.name,lvl+1)
        case Declaration():
            print(f"{ind}Declaration:")
            print_ast(ast.name,lvl+1)
            print_ast(ast.var_type,lvl+1)
        case CompoundStatement():
            print(f"{ind}CompoundStatement:")
            if ast.statements:
                for s in ast.statements:
                    print_ast(s,lvl+1)
        case Assignment():
            print(f"{ind}Assignment:")
            print_ast(ast.target,lvl+1)
            print_ast(ast.value,lvl+1)
        case If():
            print(f"{ind}If:")
            print_ast(ast.condition,lvl+1)
            print_ast(ast.true_branch,lvl+1)
            print_ast(ast.false_branch,lvl+1)
        case While():
            print(f"{ind}While:")
            print_ast(ast.condition,lvl+1)
            print_ast(ast.body,lvl+1)
        case For():
            print(f"{ind}For:")
            print_ast(ast.declaration,lvl+1)
            print_ast(ast.initial_value,lvl+1)
            print_ast(ast.limit,lvl+1)
            print_ast(ast.body,lvl+1)
        case FunctionCall():
            print(f"{ind}FunctionCall:")
            print_ast(ast.identifier,lvl+1)
            if ast.args:
                for a in ast.args:
                    print_ast(a,lvl+1)
        case Return():
            print(f"{ind}Return:")
            print_ast(ast.value,lvl+1)
        case _:
            print(f"{ind}{ast}")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def next(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        else:
            return None

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            return None

    def expect(self, expected):
        actual = self.peek()
        if self.peek().kind == expected:
            return self.next()
        else:
            raise Exception(f"Expected {expected}, got {actual}")
    
    def parse(self):
        return self.parse_program()

    def parse_program(self):
        functions = []
        while (self.pos < len(self.tokens)):
            functions.append(self.parse_function())
        return Program(functions)

    def parse_function(self):
        self.expect(TokenKind.FUNC)
        name = self.parse_identifier()
        self.expect(TokenKind.OPEN_PAREN)
        params = None
        if self.peek().kind != TokenKind.CLOSE_PAREN:
            params = self.parse_params()
        self.expect(TokenKind.CLOSE_PAREN)
        return_type = None
        if self.peek().kind == TokenKind.COLON:
            self.next()
            return_type = self.parse_identifier()
        body = self.parse_compound_statement()
        return Function(name, params, return_type, body)

    def parse_identifier(self):
        identifier = self.expect(TokenKind.ID)
        return identifier

    def parse_compound_statement(self):
        statements = []
        self.expect(TokenKind.OPEN_BRACE)
        while self.peek().kind != TokenKind.CLOSE_BRACE:
            statements.append(self.parse_statement())
        self.expect(TokenKind.CLOSE_BRACE)
        return CompoundStatement(statements)

    def parse_statement(self):
        match self.peek().kind:
            case TokenKind.FOR:
                return self.parse_for()
            case TokenKind.WHILE:
                return self.parse_while()
            case TokenKind.IF:
                return self.parse_if()
            case TokenKind.RETURN:
                self.next()
                return Return(self.parse_expression())
            case TokenKind.OPEN_BRACE:
                return self.parse_compound_statement()
            case _:
                return self.parse_basic_statement()

    def parse_if(self):
        self.expect(TokenKind.IF)
        expr = self.parse_expression()
        true_branch = self.parse_statement()
        false_branch = None
        if self.peek().kind == TokenKind.ELSE:
            self.next()
            false_branch = self.parse_statement()
        return If(expr, true_branch, false_branch)

    def parse_while(self):
        self.expect(TokenKind.WHILE)
        condition = self.parse_expression()
        body = self.parse_statement()
        return While(condition, body)
    
    def parse_for(self):
        self.expect(TokenKind.FOR)
        declaration = self.parse_parameter()
        self.expect(TokenKind.EQUAL)
        initial_value = self.parse_expression()
        self.expect(TokenKind.TO)
        limit = self.parse_expression()
        body = self.parse_statement()
        return For(declaration, initial_value, limit, body)

    def parse_params(self):
        params = []
        params.append(self.parse_parameter())
        while (self.peek().kind == TokenKind.COMMA):
            self.next()
            params.append(self.parse_parameter())

        return params

    def parse_parameter(self):
        identifier = self.parse_identifier()
        self.expect(TokenKind.COLON)
        var_type = self.parse_expression()
        return Declaration(identifier, var_type)

    def parse_declaration(self):
        self.expect(TokenKind.VAR)
        identifier = self.parse_identifier()
        self.expect(TokenKind.COLON)
        var_type = self.parse_expression()
        decl = Declaration(identifier, var_type)
        if self.peek().kind == TokenKind.EQUAL:
            self.next()
            value = self.parse_expression()
            return Assignment(decl, value)
        else:
            return decl

    def parse_basic_statement(self):
        match self.peek().kind:
            case TokenKind.VAR:
                return self.parse_declaration()
            case TokenKind.STRING | TokenKind.NUMBER:
                return self.parse_literal()
            case TokenKind.ID:
                identifier = self.parse_identifier()
                if self.peek().kind == TokenKind.OPEN_PAREN:
                    self.next()
                    args = None
                    if self.peek().kind != TokenKind.CLOSE_PAREN:
                        args = self.parse_arguments()
                    self.expect(TokenKind.CLOSE_PAREN)
                    return FunctionCall(identifier, args)
                elif self.peek().kind == TokenKind.EQUAL:
                    self.next()
                    value = self.parse_expression()
                    return Assignment(identifier, value)
                else:
                    return identifier
            case x:
                raise Exception(f"Unexpected token in statement: {x=}")
                self.next()

    def parse_expression(self):
        if self.peek().kind == TokenKind.OPEN_PAREN:
            self.next()
            expression = self.parse_expression()
            self.expect(TokenKind.CLOSE_PAREN)
            return expression
        if self.peek().kind == TokenKind.ID:
            identifier = self.parse_identifier()
            if self.peek().kind == TokenKind.OPEN_PAREN:
                self.next()
                args = []
                if self.peek().kind != TokenKind.CLOSE_PAREN:
                    args = self.parse_arguments()
                    self.expect(TokenKind.CLOSE_PAREN)
                return FunctionCall(identifier, args)
            else:
                return identifier
        else:
            return self.parse_literal()

    def parse_arguments(self):
        args = []
        args.append(self.parse_expression())
        while self.peek().kind == TokenKind.COMMA:
            self.next()
            args.append(self.parse_expression())
        return args

    def parse_literal(self):
        if self.peek().kind == TokenKind.STRING or self.peek().kind == TokenKind.NUMBER:
            return self.next()
        return None
