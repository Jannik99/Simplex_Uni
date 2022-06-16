from parser import *

import numpy as np

test_a = np.array([ [1, 1, 3], [2, 4, 8], [2, 3, 0]])
test_b = np.array([[1,1,1,4,5,5], [4,1,4,3,3,9], [5,1,1,4,4,15], [1,3,3,5,2, 0]])
test_c = np.array([[4,5,4,1,5,2,7,2,9,22], [9,3,8,5,4,1,8,2,2,55], [4,8,1,7,8,6,6,3,9,24], [8,8,6,6,4,4,9,2,5,46], [4,2,3,1,5,9,6,4,4,6], [9,3,2,8,1,3,7,7,5,11], [7,8,3,5,3,1,3,6,8,59], [9,4,6,4,1,3,3,8,7,17], [9,5,3,8,6,8,5,3,1, 0]])


def find_pivot(table):
  print("Finding pivot")
  pivot_col_index = np.argmax(table[-1])
  pivot_row_index = np.argmin(np.divide([row[-1] for row in table][:-1], table[:-1, pivot_col_index]))
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
      table[i] = table[i]-(table[i, pivot_col_index]*table[pivot_row_index]) # Pivotcolelement to 0 by:  row = row - (Pivotcolnelement * pivotrow)
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
    print("Solving Table")
    print(table)
    table = addSlackVariables(table)
    print(table)
    while(not check_if_solved(table)):
      table = single_run(table, *find_pivot(table))
      print(table)
    print("Table is solved \n", table)
    
    get_solution_from_solved_table(table)
  return table

def get_solution_from_solved_table(table):
  x = []
  z = table[-1, -1] * (-1) # *(-1) because 
  for i in range(len(table)-1):
    if(table[i][i] != 0):
      x.append(table[i,-1]/table[i,i])
    else:
      x.append(0)
    print("x"+str(i), " = ", x[-1])
  print("z = ", z)
  return x, z

def solve_all():
  parsedBenchmarks = getParsedBenchmarks()
  solutions = []
  for i, parsed in enumerate(parsedBenchmarks):
    print("Benchmark: ", i)
    solutions.append(solve(parsed)) 

# solve_all()

solve((test_a, "max"))
# solve((test_b, "min"))
# solve((test_c, "min"))
