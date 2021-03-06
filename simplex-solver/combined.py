import os
from cmath import isclose
from inspect import isclass
from parser import *

import numpy as np

np.set_printoptions(edgeitems=30, linewidth=100000, suppress=True) # Set print options for numpy to use more space in Terminal

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
    rows[-1].append(0)
    return np.array(rows), min_or_max



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

test_a = np.array([ [1, 1, 3], [2, 4, 8], [2, 3, 0]])
test_b = np.array([[1,1,1,4,5,5], [4,1,4,3,3,9], [5,1,1,4,4,15], [1,3,3,5,2, 0]])
test_c = np.array([[4,5,4,1,5,2,7,2,9,22], [9,3,8,5,4,1,8,2,2,55], [4,8,1,7,8,6,6,3,9,24], [8,8,6,6,4,4,9,2,5,46], [4,2,3,1,5,9,6,4,4,6], [9,3,2,8,1,3,7,7,5,11], [7,8,3,5,3,1,3,6,8,59], [9,4,6,4,1,3,3,8,7,17], [9,5,3,8,6,8,5,3,1, 0]])

def printTable(table, msg=None):
  # print(msg + "\n" if msg != None else "", np.ceil(table))
  print(msg + "\n" if msg != None else "", table)

def find_pivot(table):
  print("Finding pivot")
  pivot_col_index = np.argmax(table[-1, :-1]) # Find index of column with highest value
  pivot_rows_value = np.divide([row[-1] for row in table][:-1], table[:-1, pivot_col_index])
  pivot_row_index = np.argmin(pivot_rows_value[pivot_rows_value!=0]) 
  
  print("Pivot row index: " + str(pivot_row_index))
  print("Pivot column index: " + str(pivot_col_index))
  print("Pivot element: " + str(table[pivot_row_index][pivot_col_index]))
  return (pivot_row_index, pivot_col_index, table[pivot_row_index, pivot_col_index])
    
def transposeTable(table):
  print("Transposing table")
  return np.transpose(table) 
    
def addSlackVariables(table):
  print("Adding slack variables")
  tableshape = table.shape
  newTableshape = (tableshape[0], tableshape[1] + tableshape[0] - 1) # New table has to be (rows, columns + rows - 1)
  newTable = np.zeros(newTableshape) # Initialize new table with zeros
  np.fill_diagonal(newTable[:, tableshape[1]-1:], 1) # Fill diagonal with ones
  newTable[:, 0:tableshape[1]-1] = table[:, 0:tableshape[1]-1] # Copy old table into new table
  newTable[:, -1] = table[:, -1] # Copy last column of old table into new table
  return newTable

def single_run(table, pivot_row_index, pivot_col_index, pivot_element):
  print("Single run of simplex")

  table[pivot_row_index] = table[pivot_row_index]/pivot_element # make pivot element 1 by dividing pivot row / pivot element
  for i in range(len(table)): # for every row 
    if(i != pivot_row_index): # except for pivot row
      # if(table[i, pivot_col_index] != 0):
      table[i] = table[i]-(table[i, pivot_col_index]*table[pivot_row_index]) # Pivotcolelement to 0 by:  row = row - (Pivotcolelement * pivotrow)
  return table


def check_if_solved(table):
  for el in table[-1]:
    if(el > 0):
      return False
  return True

def solve(parsed):
  table = parsed[0]
  if(parsed[1] == "min"):
    table = transposeTable(table)
  
  if check_if_solved(table):
    print("Table is already solved")
  else:  
    printTable(table, "Solving Table")
    table = addSlackVariables(table)
    printTable(table)
    while(not check_if_solved(table) ):
      table = single_run(table, *find_pivot(table))
      printTable(table)
    printTable(table, "Solved Table:")
    
  return get_solution_from_solved_table(table, parsed[1])

def get_solution_from_solved_table(table, max_or_min):
    x = []
    z = table[-1, -1] * (-1) # *(-1) because I cannot transform, since I do not use a variable 
    if max_or_min == "max":
        for i in range(len(table)-1):
            if(table[i][i] != 0):
                x.append(table[i,-1]/table[i,i])
            else:
                x.append(0)
            print("x"+str(i), " = ", x[-1])
    else:
        num_rows, num_cols = np.shape(table)
        start_index = num_cols - num_rows
        stop_index = num_cols - 1
        print("start", start_index)
        print("stop", stop_index)
        for i in range(stop_index - start_index):
            x.append(table[-1, start_index + i] * -1)
            print("x"+str(i), " = ", x[-1])
    print("z = ", z)
    return x, z

def solve_all():
  parsedBenchmarks = getParsedBenchmarks()
  solutions = []
  for i, parsed in enumerate(parsedBenchmarks):
    print("Benchmark: ", i)
    solutions.append(solve(parsed))
    print("All Solutions:")
    for i in range(len(solutions)):
        print("Solution ", i, ":", solutions[i])

solve_all()
# solve((test_a, "max"))
# solve((test_b, "min"))
# solve((test_c, "min"))
