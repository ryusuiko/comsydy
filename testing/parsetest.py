from ast import parse, dump

with open("10.py", 'r') as file:
    program = file.read()

print(dump(parse(program), indent=4))
