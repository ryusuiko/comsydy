import sys
from ast import literal_eval
from subprocess import run
import os.path
import json
from src.linter import *

def iscmdi(userinput):

    chars = ";|&^*#"

    for char in chars:
        if char in userinput:
            return 1

    return 0

pythonfile = 0
while pythonfile == 0:

    pythonfile = input("Print path to python file: ")
    if (pythonfile == "") or iscmdi(pythonfile) or (not os.path.exists(pythonfile)):
        pythonfile = 0
        sys.stderr.write("Incorrect path")
    else:
        with open(pythonfile, 'r') as file:
            program = file.read()

#### Static Analysis ####

# Two ways:
# 1) Do ast.parse() and make abstract syntax tree
# 2) Iterate through code line by line and "do analysis"

# 1st way
test = parse(program).body
expression = ''.join(dump(test[3]).split("\n"))

# 2nd way
# for line in range(len(program)):
#     if program[line][0] == "#":
#         print(line+1, "comment")
#
#     if re.match(FUNCTION_DEF, program[line]):
#         print(line+1, "function")
#     if re.match(VARIABLE, program[line]):
#         print(line+1, "var")
#     if re.match(IMPORT_MODULE, program[line]):
#         print(line+1, "import")
#     if re.match(CLASS, program[line]):
#         print(line+1, "class")

#### Dynamic Analysis ####

# Use exec() to execute python code
# execute only some "blocks" that contain input