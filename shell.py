import argparse

parser = argparse.ArgumentParser(description="""
CodeAnalyser is a Python script which parses Python code to check it for
possible command injection vulnerabilities.\n
WARNING: IT'S DANGEROUS TO PARSE UNTRUSTED CODE!\n
Use flag -n or --new to specify existing rule to change some properties.
""")
parser.add_argument("-f", "--file", type=str, help="Specifies a path to Python file")
parser.add_argument("-l", "--list", help="Prints out all rules", action="store_true")
parser.add_argument("-r", "--rule", type=str, help="Specifies existing rule to rules.json")
parser.add_argument("-d", "--dynamic", type=str, help="Adds new argument to DAST tool")
parser.add_argument("-N", "--Name", type=str, help="Adds name to a rule in -n")
parser.add_argument("-D", "--Description", type=str, help="Adds description to a rule in -n")
parser.add_argument("-R", "--Recommendation", type=str, help="Adds recommendation to a rule in -n")
args = parser.parse_args()