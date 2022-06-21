from parser import *

import time
import numpy as np

def solve(array):
    # Transponiere weil Minimierungsproblem
    transposed = np.transpose(array)

    # calculate how many extra variables we need
    num_rows, num_cols = transposed.shape
    needed_variables = num_rows - 1
    new_column_size = num_cols + needed_variables
    new_row_size = num_rows

    new_matrix = np.zeros((new_row_size, new_column_size))

    # Fülle mit Schlupfvariablen
    np.fill_diagonal(new_matrix[: ,num_cols-1:], 1)
    # copy transposed matrix into new big matrix
    new_matrix[:, 0:num_cols - 1] = transposed[:, 0:num_cols - 1]
    # access last column of new matrix and paste last column from transposed matrix
    new_matrix[:, -1] = transposed[:, -1]

    print(f'Initial Matrix \n {new_matrix}')
    iterations = 1
    finished = False
    while finished is False:
        new_matrix = iterate(new_matrix)
        last_row = new_matrix[-1, :]
        last_row_without_solution = last_row[:-1]
        print(f'After {iterations} iterations new matrix \n {new_matrix}')
        iterations += 1
        print(f'Überprüfung: {last_row_without_solution}')
        largest_element = np.max(last_row_without_solution)
        print(f'Largest Element: {largest_element}')
        finished = True if np.max(last_row_without_solution) <= 0 else False
        print(f'Finished variable {finished}')
        time.sleep(1)
        
    base_swap = new_matrix[:, num_cols-1:]
    #print(f'base_swap \n {base_swap}')

    print_solution(base_swap)
    
    
def iterate(matrix):

    last_row = matrix[len(matrix)-1 , :-1]
    # find position of largest element in last row
    index_largest_element = np.argmax(last_row)
    print(f'Last row {last_row}')
    print(f'Largest element {index_largest_element}')
    pivot_column = matrix[:-1, index_largest_element]

    # take last columns and divide it with pivot column
    last_column = matrix[:-1, -1]
    
    with np.errstate(divide="ignore", invalid="ignore"):
        temporary_solution_column = np.true_divide(last_column, pivot_column, where=pivot_column!=0)

    #tmp = last_column / pivot_column
    print(f'Ergebnisspalte: {temporary_solution_column}')
    # find position of smallest element in temporary column
    # TODO: GRÖ?ER ALS 0
    index_smallest_element = np.argmin(temporary_solution_column, axis = 0)

    pivot_position = index_smallest_element, index_largest_element
    print(f'Position Pivot Element {pivot_position}')
    pivot_row = matrix[index_smallest_element, :]
    print(f'Pivot Zeile {pivot_row}')
    pivot_column = matrix[:, index_largest_element]
    print(f'Pivot Spalte {pivot_column}')
    pivot_element = matrix[index_smallest_element, index_largest_element]
    print(f'Pivot Element: {pivot_element}')
    
    print("Pivot Reihe durch Pivot Element um dieses auf 1 zu bringen")
    pivot_row /= pivot_element 
    # Pivot Element ist jetzt auf 1. Jedes Element da drunter muss  0 werden.

    print(f'Neue Pivot Reihe {pivot_row}' )

    pivot_element = matrix[index_smallest_element, index_largest_element]
    print(f'Neues Pivot Element {pivot_element}')

    row_index = 0
    # Durchlaufe jede Reihe
    for row in matrix:
        # Wenn die Reihe nicht die Pivot Reihe ist
        if row_index != pivot_position[0]:
            # Berechne Koeffizient
            coefficient = matrix[row_index, pivot_position[1]]
            row = row - pivot_row * coefficient
            matrix[row_index, :] = row
        row_index += 1
    return matrix

def print_solution(matrix):
    solution_row = matrix[-1, :]
    iterations = 0
    for element in solution_row:
        if iterations != solution_row.size - 1:
            print(f'x{iterations} = {element*-1}')
        else:
            print(f'Z: {element*-1}')
        iterations +=1

parsed_benchmarks = getParsedBenchmarks()
benchmarks = []
for i, parsed in enumerate(parsed_benchmarks):
    benchmarks.append(parsed[0])

for benchmark in benchmarks:
    solve(benchmark)

#a = np.array([[1,1,1,4,5,5], [4,1,4,3,3,9], [5,1,1,4,4,15], [1,3,3,5,2,0]])
#b = np.array([[2,2,2,5,7,8,2,5,51], [4,4,3,1,2,7,5,1,1], [8,5,3,6,6,2,2,6,26], [7,8,5,7,8,1,4,7,38], [1,6,6,6,2,6,8,7,0]])
#c = np.array([[4,5,4,1,5,2,7,2,9,22], [9,3,8,5,4,1,8,2,2,55], [4,8,1,7,8,6,6,3,9,24], [8,8,6,6,4,4,9,2,5,46], [4,2,3,1,5,9,6,4,4,6], [9,3,2,8,1,3,7,7,5,11], [7,8,3,5,3,1,3,6,8,59], [9,4,6,4,1,3,3,8,7,17], [9,5,3,8,6,8,5,3,1, 0]])
#ki_15 = np.array([[11,1,11,12,11,9,1,2,3,13,6,12,10,7,6,78], [1,8,1,3,15,9,5,3,7,9,1,8,11,6,15,144], [7,7,7,15,3,8,8,12,9,11,6,6,14,4,5,79], [11,9,2,8,6,7,2,12,10,15,1,11,2,15,12,25], [14,9,7,14,2,5,3,4,1,5,6,9,1,2,4,71], [9,6,1,6,2,11,7,13,8,9,7,14,8,10,9,27], [3,7,8,7,2,15,3,8,15,7,9,4,14,3,10,179], [12,3,6,11,4,10,1,13,1,12,7,9,9,9,4,97], [8,9,3,8,14,14,13,1,7,7,13,13,3,5,2,138], [1,6,1,13,14,8,15,1,8,14,6,7,2,7,4,0]])
#solve(ki_15)

