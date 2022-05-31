import os
from calendar import c
from cmath import log
from inspect import _void

benchmark_dir = "./benchmarks"

def __getAllFileNames(benchmark_dir) -> list:
    '''
    reads all .txt files in the given directory ./benchmarks and returns a list like this: filename.txt
    '''
    files = []
    for file in os.listdir(benchmark_dir):
        if file.endswith(".txt"):
            files.append(file)
    return files

def __getFileContents(benchmark_dir, file_name) -> list:
    '''
    parses the file and returns a list of all lines in the file
    '''
    file = open(benchmark_dir + "/" + file_name, "r")
    
    lines = file.readlines()
    file.close()
    return lines
    
def __parseFileContents(contents : list):
    '''
    gets the objective function, constraints and if its a minimization or maximization problem.
    '''
    row_string = []
    last_row: str = ""
    min_or_max = ""
    for line in contents:
        if line.startswith("//"):
            continue
        if line.startswith(" +") or line.startswith(" -"):
            row_string.append(line)
        elif line.startswith("min:"):
            min_or_max = "min"
            last_row = line.strip("min:")
        elif line.startswith("max:"):
            min_or_max = "max"
            last_row = line.strip("max:") 

    
    row_string.append(last_row)
    rows = []
    for row in row_string:
        row = row.strip()
        coefficients = []
        parts = row.split(" ")
        for i in range(len(parts)):
            if parts[i] == "+":
                coefficients.append(int(parts[i+1].split("x")[0].strip("*")))
                
            elif parts[i] == "-":
                coefficients.append(-int(parts[i+1].split("x")[0].strip("*")))
                
            elif parts[i] == ">=" or parts[i] == "<=":
                coefficients.append(int(parts[i+1].strip(";")))
            
            if(i == len(parts) - 1):
                rows.append(coefficients)
    return rows, min_or_max



def getParsedBenchmarks() -> list:
    parsedBenchmarks = []
    filenames = __getAllFileNames(benchmark_dir)
    for filename in filenames:
        print("Parsing file: " + filename)
        contents = __getFileContents(benchmark_dir, filename)
        rows, min_or_max = __parseFileContents(contents)
        print("Ready!\nContents are:")
        print(rows)
        print("\n")
        parsedBenchmarks.append((rows, min_or_max))
    return parsedBenchmarks

