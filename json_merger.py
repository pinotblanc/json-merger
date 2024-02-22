import sys
import json

########## pino 22.02.24 ##########
#
# the script takes any amount of nested
# json files with int values and merges
# them into one, preserving all key paths
# 
# usage: json_merger <operation (+, - and * supported)> <file1.json> ... <fileN.json>
#

# iterates over all files and adds the values to the result dict
def json_merge(*paths):

    result = {}

    for path in paths:

        with open(path, 'r') as file:

            data = json.load(file)
            rec_sum(data, result, [])

    return result

# adds a value to a key path in a recursive dict
def add_at_path(value, result, result_path):

    curr = result

    for depth, key in enumerate(result_path):
        if depth == len(result_path)-1:
            # making sure not to overwrite a value
            if key in curr.keys():
                if op == "+":
                    curr[key] += value
                elif op == "-":
                    curr[key] -= value
                else:
                    curr[key] *= value
            else:
                curr[key] = value
        else:
            if key not in curr.keys():
                curr[key] = {}
            curr = curr[key]

# takes nested dict and recursively sums up int values from same keys paths
# to the same key path in result dict
def rec_sum(data, result, result_path):

    for key, value in data.items():

        # check if we reached bottom level key
        if isinstance(value, int):
            add_at_path(value, result, result_path + [key])

        # if not at bottom level, add key to result_path
        elif isinstance(value, dict):

            rec_sum(value, result, result_path + [key])

        # should never be reached
        else:
            print("ERROR, value " + value + " is not an int!")
            sys.exit(1)

    

if __name__ == "__main__":

    # check for help flag
    if sys.argv[1] in ["-help", "-h", "help", "h"]:
        print("usage: json_merger <operation (+, - and * supported)> <file1.json> ... <fileN.json>")
        sys.exit(0)

    # check for valid operator
    op = sys.argv[1]
    if op not in ["+", "-", "*"]:
        print("error: invalid operation (only +, - and * supported)")
        sys.exit(1)

    paths = sys.argv[2:]

    # check if json was given
    if len(paths) < 2:
        print("error: less than 2 json files")
        sys.exit(1)

    merged_dict = json_merge(*paths)

    with open('output.json', 'w', encoding='utf-8') as out:
        json.dump(merged_dict, out, ensure_ascii=False, indent=4)
