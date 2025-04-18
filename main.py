import re
import sys
from subprocess import run
import os.path
import json
from src.linter import *
import shell

def main():
    program = list()
    pythonfile = shell.args.file
    with open(pythonfile, 'r') as file:
        program = file.readlines()

    fullprogram = ''.join(program)
    globalvars = findvars(program)
    modulesinfo = findmodules(program)
    modulelines = str()

    def modules():
        nonlocal modulelines
        for line in program:
            if moduleline(line):
                modulelines = line + "\n"

    modules()

    #### Static Analysis ####

    # C:\Users\pinok\PycharmProjects\ast_example.py

    foundErrorAtSAST = False

    def SAST():
        nonlocal foundErrorAtSAST
        test = parse(line)
        expression = ''.join(dump(test))
        a = fullastparse(expression)
        if a != ([], []):
            foundErrorAtSAST = True
        for rule in a[1]:
            print(f"""Line {i}: {program[i - 1]}
{json_load["rules"][rule]["name"]}
{json_load["rules"][rule]["description"]}
{json_load["rules"][rule]["recommendation"]}
                    """)

    def magicDAST(funcname: str, funccall: str, funcbody: str, vars: list, varsbody: str):
        toExec = modulelines + '\n' + varsbody + '\n' + funcbody + '\n' + funccall

        #### There DAST starts ####

        with open("./src/dynamic.txt", 'r') as file:
            inputs = file.read()

        inputs = inputs.split('\n')

        try:
            for inp in inputs:
                output = exec(toExec.replace("input()", f"\"{inp}\""))
                if run("whoami") in output:
                    varsForOut = str(*vars)
                    print(f"""
                    Command Injection vulnerable function {funcname}()
                    Variables: {varsForOut}
                    Test input: {inp}
                    """)
        except Exception:
            pass

    print("- Static Analysis -\n")
    i = 0
    for line in program:
        i += 1
        try:
            SAST()
        except IndentationError:
            if ("def" not in line) and ("class" not in line):
                while " " in line[0]:
                    line = line[1:]
                SAST()

    if foundErrorAtSAST == False:
        print("No errors found in code")

    #### Extracting functions ####

    Functions = list() # str
    funcBlock = False
    currentFuncBlock = str()

    for line in fullprogram.split('\n'):
        line = line + '\n'

        try:
            if (funcBlock == True) and (line[0] == ' ' or '\t' in line):
                currentFuncBlock = currentFuncBlock + line
            elif isFunc(line):
                funcBlock = True
                currentFuncBlock = currentFuncBlock + line
            else:
                funcBlock = False
                if currentFuncBlock != '':
                    Functions.append(currentFuncBlock)
                currentFuncBlock = ''
        except IndexError:
            funcBlock = False

    #### Dynamic Analysis ####

    print("- Dynamic Analysis -\n")
    for func in Functions:

        funcName = getFuncName(func.split("\n")[0])
        funcVars = getFuncVars(func.split("\n")[0])
        currentVars = list()
        requiredVarsForDAST = list()
        notRequired = list()
        notRequiredBody = list()
        foundFuncCalls = re.findall(rf"{funcName}\(.*\)\n", fullprogram)

        for funcCall in foundFuncCalls:
            currentVars = getFuncVars(funcCall)

        for var in currentVars:
            if var in globalvars:
                requiredVarsForDAST.append(var)
            else:
                notRequired.append(var)

        #### Preparing for DAST ####

        varsbody = list()
        for line in program:
            try:
                var = re.match(r"[a-zA-Z_0-9]*.*=.*input\(.*\).*", line).group(0)
                varsbody.append(var)
            except AttributeError:
                pass

        if (notRequired != []) and (not ("input()" in notRequired)):
            for var in notRequired:
                notRequiredBody.append(re.findall(rf"{var}.*=.*", fullprogram)[0])

        varsbody = "\n".join(varsbody+notRequiredBody)

        if foundFuncCalls != []:
            magicDAST(funcName, foundFuncCalls[0], func, requiredVarsForDAST, varsbody)
        else:
            print(f"No calls for function {funcName}()")

if __name__ == "__main__":

    if shell.args.file:
        main()

    if shell.args.list:
        rules = list()
        for rule in json_load['rules']:
            rules.append(rule)
        print(*rules, sep='\n')

    if shell.args.rule:

        rule = shell.args.rule
        if rule in json_load:
            if shell.args.Name:
                pass
            if shell.args.Description:
                pass
            if shell.args.Recommendation:
                pass

    if shell.args.dynamic:

        with open("./src/dynamic.txt", 'a') as file:
            file.write('\n' + shell.args.dynamic)