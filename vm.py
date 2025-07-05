import parser, lexer
from enum import Enum, auto

class PrimitiveType(Enum):
    type_int = auto()
    type_char = auto()

class Type:
    pass

class StructType:
    pass

class ShlangVM:
    globals = []
    scopes = []
    types = [PrimitiveType.type_int, PrimitiveType.type_char]

    def __init__(self):
        pass

    def interpret_program(self, program):
        self.functions = program.functions
        main = None
        for f in self.functions:
            if f.name.text == "main":
                main = f

        if f:
            self.interpret_function(f)
        else:
            print("ERROR: No main function found")

    def interpret_function(self, function):
        current_scope = []
        for param in function.parameters:
            if param.var_type in self.types
