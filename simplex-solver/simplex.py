from parser import *

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


    def check_for_finish(matrix):
        last_column = matrix[:, -1]
        finished = True if np.max(last_column) < 0 else False
        return finished

    print(f'First Iteration: \n {iterate(new_matrix)}')


    solution = iterate(new_matrix)
    finished = check_for_finish(solution)
    print(f'Second Iteration \n {solution}')

    base_swap = solution[:, num_cols-1:]
    print(f'base_swap \n {base_swap}')

    print_solution(base_swap)

    
    
def iterate(matrix):
    #print(f"Searching Pivot Column, Row, Element on \n {matrix}")
    last_row = matrix[len(matrix)-1 , :-1]
    # find position of largest element in last row
    index_largest_element = np.argmax(last_row, axis = 0)
    pivot_column = matrix[:-1, index_largest_element]

    # take last columns and divide it with pivot column
    last_column = matrix[:-1, -1]
    temporary_solution_column = np.divide(last_column, pivot_column, where=pivot_column!=0)
    #tmp = last_column / pivot_column
    print(f'Ergebnisspalte: {temporary_solution_column}')
    #matrix[:-1, -1] = tmp
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
    return np.round(matrix, decimals=2)

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
#solve(a)

