from parser import *

import numpy as np

test_a = [ [1, 1, 3], [2, 4, 8], [2, 3, 0]]
test_b = [[1,1,1,4,5,5], [4,1,4,3,3,9], [5,1,1,4,4,15], [1,3,3,5,2]]


def find_pivot(parsed):
    print("Searching for pivot column")
    # find position of largest element in last row
    pivot_col_index = np.argmax(parsed[-1])
    pivot_column = [row[pivot_col_index] for row in parsed][:-1]
    print("Pivot column: ", pivot_column)
    # find pivot row
    print("Searching for pivot element")
    (calculating_pivot_element, pivot_row_index) = (parsed[0,-1]/pivot_column[0], 0)
    for i, item in enumerate(pivot_column):
        if(item != 0):
            element = parsed[i, -1]/item
        
        if(element < calculating_pivot_element):
            calculating_pivot_element = element
            pivot_row_index = i

    pivot_element = parsed[pivot_row_index, pivot_col_index]
    print("Pivot col: ", pivot_col_index)
    print("Pivot row: ", pivot_row_index)
    print("Pivot Element: ", pivot_element)
    return (pivot_row_index, pivot_col_index, pivot_element)
        

def makeTable(parsed):
    print("Generating table")
    # make table from parsed data and add space for slack variables
    table = np.zeros((len(parsed), (len(parsed)*2)-1))
    for i, row in enumerate(parsed):
        for j, item in enumerate(row):
            if(j < len(row)-1):
                table[i, j] = item
            else:
                table[i, -1] = item
    print(table)
    # Fill slack variables
    print ("Filling slack variables")
    for i in range(len(table)):
        index_becoming_one = len(table[0])-(len(table)-i)
        if(i != len(table)-1):
            table[i, index_becoming_one] = 1
    print(table)
    return table


def single_run(table, pivot_row_index, pivot_col_index, pivot_element):
    # Making pivot element 1
    print("Making pivot element 1")
    table[pivot_row_index] = table[pivot_row_index]/pivot_element
    print(table)
    # Making pivot column 0
    print("Making pivot column 0")
    for i in range(len(table)):
        if(i != pivot_row_index):
            table[i] = table[i]-(table[i, pivot_col_index]*table[pivot_row_index])
    print(table)
    return table

def check_if_solved(table):
    ret = True
    for el in table[-1]:
        if(el > 0):
            ret = False
    return ret

def solve(parsed):
    table = makeTable(parsed)
    while(True):
        pivot_row_index, pivot_col_index, pivot_element = find_pivot(table)
        table = single_run(table, pivot_row_index, pivot_col_index, pivot_element)
        if(check_if_solved(table)):
            break
    
    z = table[-1, -1]
    x = []
    print("SOLVED !!")
    print("z = " , table[-1, -1])
    for i in range(len(parsed)-1):
        x.append(table[i, -1]/table[i, i])
        print("x"+str(i+1), " = ", x[-1])

    print ("Table: \n", table)
    return table, x, z

    

# Running everything
parsedBenchmarks = getParsedBenchmarks()
solutions = []
for i, parsed in enumerate(parsedBenchmarks):
    print("Benchmark: ", i)
    solutions.append(solve(parsed[0]))

# solve(test_b)

print("Solutions: ", solutions)
