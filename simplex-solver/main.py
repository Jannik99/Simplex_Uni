import copy
from cmath import isclose
from inspect import isclass
from parser import *

import numpy as np

np.set_printoptions(edgeitems=30, linewidth=100000, suppress=True) # Set print options for numpy to use more space in Terminal

def printTable(table, msg=None):
  print(msg + "\n" if msg != None else "", table)

def find_pivot(table):
  print("Finding pivot")
  pivot_col_index = np.argmax(table[-1, :-1]) # Find index of column with highest value
  print("old rows_value", np.divide([row[-1] for row in table][:-1], copy.copy(table[:-1, pivot_col_index])))
  pivot_rows_value = []
  for i in range(len(table)-1):
    if(table[i][pivot_col_index] > 0 and table[i][-1] != 0):
      pivot_rows_value.append(np.round(table[i][-1]/table[i][pivot_col_index], 2))
    else:
      pivot_rows_value.append(0)

  print("new rows_value", pivot_rows_value)
  pivot_row_index = None

  for i in range(len(pivot_rows_value)):
    if(pivot_rows_value[i] != 0):
      if(pivot_row_index == None):
        pivot_row_index = i
      if(pivot_rows_value[i] < pivot_rows_value[pivot_row_index]):
        pivot_row_index = i
  
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
