from ast import parse, dump, unparse
import json
import re

#### All (almost) expressions for proper input ####

# Main
IMPORT_MODULE = "Import(*)"

VARIABLE = "Assign(*)"
INPUT = "(*, *id='input')"
INPUT_VARIABLE = "Assign(*, *id='input')"
BODY = "body[*]"

# Functions
FUNCTION_DEF = "FunctionDef*"
EXPRESSION = "Expr*"
PASS = "Pass()"
BREAK = "Break()"
CONTINUE = "Continue()"
RETURN = "Return*"
CALL_FUNC = "Call*" # We're mostly interested in func with Name ID = "input"

# Class
CLASS = "ClassDef*"

GLOBAL_VARIABLES = list()

def separateInput():
    pass

def formBlock():
    pass

def formBlockList():
    pass

def taint():
    pass

class Linter:

    pass