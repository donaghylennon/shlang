import parser

def gen_program(program):
    output = "format ELF64 executable 3\n"
    output += "entry main\n"
    output += "segment readable executable\n"
    data_segment = "segment readable"
    for func in program.functions:
        output += gen_function()

def gen_function(function, output):
    output += function.name + ":"
