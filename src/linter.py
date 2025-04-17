from ast import parse, dump, unparse
import json
import re

with open("./src/rules.json", 'r') as json_file:
    json_file = json_file.read()
    json_load = json.loads(json_file)

del json_file

def findvars(program: list):
    test = list()
    for line in program:
        try:
            var = re.match(r"[a-zA-Z_0-9]*.*=.*input\(.*\).*", line).group(0)
            test.append(var.split(" ")[0])
        except AttributeError:
            pass
    return test

def findmodules(program: list):
    modules = list() # [module] or [module, as]
    from_modules = dict() # module: [funcs]
    for line in program:
        try:
            text = line.split(' ')
            module_add = 1
            if text[0] == "import":
                text = text[1:]
                for i in range(len(text[1:])):
                    if text[i] != "as":
                        if text[i-1] == "as":
                            continue
                        if text[i+1] == "as":
                            modules.append([text[i], text[i+2]])
                        else:
                            if text[i][-1] == ',':
                                modules.append(text[i][:-1])
                            else:
                                modules.append(text[i])
            elif text[0] == "from":
                text = text[1:]
                thislinemodules = [] # Запоминаем названия модулей в данной строке
                for i in range(len(text[1:])):
                    if "import" in text[i]:
                        module_add = 0
                    elif (text[i] != "as") and (module_add == 1):
                        if text[i + 1] == "as":
                            thislinemodules.append((text[i], text[i + 1]))
                            from_modules[(text[i], text[i + 1])] = []
                        else:
                            if text[i][-1] == ',':
                                thislinemodules.append(text[i][:-1])
                                from_modules[text[i][:-1]] = []
                            else:
                                thislinemodules.append(text[i])
                                from_modules[text[i]] = []
                    else:
                        if text[i] != "as":
                            if text[i - 1] == "as":
                                continue
                            elif text[i + 1] == "as":
                                for module in thislinemodules:
                                    from_modules[module].append([text[i], text[i+2]])
                            else:
                                if text[i][-1] == ',':
                                    for module in thislinemodules:
                                        from_modules[module].append(text[i][:-1])
                                else:
                                    for module in thislinemodules:
                                        from_modules[module].append(text[i])
            else:
                pass
        except AttributeError:
            pass
    return modules, from_modules

def fullastparse(program):

    matches = list()
    rules_order = list()

    for rule in json_load["rules"]:

        name_of_rule = rule
        rule = json_load["rules"][rule]
        re_patterns = [pattern for pattern in rule["regex-patterns"]]

        # Перебираем регулярные выражения в правиле
        for pattern in re_patterns:
            match = rule["regex-patterns"][pattern]
            test = re.findall(match, program)
            for group in test:
                if group != '':
                    matches.append(group)
                    rules_order.append(name_of_rule)

    return matches, rules_order

def taint(line, vars):
    """
    Taint-анализ проверяет наличие переменных с вводом пользователя
    :param line:
    :param vars:
    :return:
    """
    for var in vars:
        if re.match(rf"Name\(id='{var}'", line):
            return True

def isFunc(line: str):
    if re.match(r"def [a-zA-Z0-9_]*\(.*\):.*", line):
        return True

def isClass(line: str):
    if re.match(r"class [a-zA-Z0-9_]*\(.*\):.*", line):
        return True

def getFuncName(line: str):
    return re.findall(r" .*\(", line)[0].replace('(', '').replace(' ', '')

def getFuncVars(line: str):
    funcvars = list()
    for group in re.findall("\(.*\)", line):
        formatted = group.split(" ")
        # Getting rid of brackets ( and )
        formatted[0] = formatted[0][1:]
        formatted[-1] = formatted[-1][:-1]
        for var in formatted:
            funcvars.append(var.replace(',', ''))
    return funcvars

def classAnalyze(line):
    if re.match(r"class [a-zA-Z0-9_]*\(.*\):.*", line):
        pass