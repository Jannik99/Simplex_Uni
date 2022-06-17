import numpy as np

def solve(array):
    
    # TODO: Transponiere nur weil Minimierungsproblem ist.. Anpassbar
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

    iterations = 0
    new_matrix = search_pivot_position(new_matrix)
    iterations += 1
    print(f'Matrix: {new_matrix}')
    print(f'Finished: {check_for_finish(new_matrix)}')
    new_matrix = search_pivot_position(new_matrix)
    iterations += 1
    print(f'Matrix: {new_matrix}')
    print(f'Finished: {check_for_finish(new_matrix)}')

def search_pivot_position(matrix):
    print(f"Searching Pivot Column, Row, Element on \n {matrix}")
    last_row = matrix[len(matrix)-1 , :-1]
    # find position of largest element in last row
    index_largest_element = np.argmax(last_row, axis = 0)
    pivot_column = matrix[:-1, index_largest_element]

    # take last columns and divide it with pivot column
    last_column = matrix[:-1, -1]
    print(f'Last column: {last_column}')
    print(f'Pivot Column: {pivot_column}')
    tmp = np.divide(last_column, pivot_column, where=pivot_column!=0)
    #tmp = last_column / pivot_column
    matrix[:-1, -1] = tmp
    # find position of smallest element in temporary column
    # TODO: GRÖ?ER ALS 0
    index_smallest_element = np.argmin(tmp, axis = 0)

    pivot_position = index_smallest_element, index_largest_element
    print(f'Position Pivot Element {pivot_position}')
    pivot_row = matrix[index_smallest_element, :]
    print(f'Pivot Zeile {pivot_row}')
    pivot_column = matrix[:, index_largest_element]
    print(f'Pivot Spalte {pivot_column}')
    pivot_element = matrix[index_smallest_element, index_largest_element]
    print(f'Pivot Element: {pivot_element}')
    
    print("Pivot Reihe durch Pivot Element um dieses auf 1 zu bringen")
    pivot_row[:-1] /= pivot_element 
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
            print(f'row {row} - pivot_row {pivot_row} * coefficient {coefficient}')
            row = row - pivot_row * coefficient
            print(f'new row {row}')
            matrix[row_index, :] = row
        row_index += 1

        # 1/5 - x*pivot_reihe = 0
        # 1/5 = x*pivot_reihe
        # 1/5/pivot_reihe = x 
    

    # Reihe = Reihe - Koeffizient * Pivot_reihe
    # Koeffizient = matrix[row_index, pivot_position[1]]

    # Zeile - Element über/drunter dem PivotELement * PivotElement
    # TODO: NACHRECHNEN...
    return np.round(matrix, decimals=7)

    
a = np.array([[1,1,1,4,5,5], [4,1,4,3,3,9], [5,1,1,4,4,15], [1,3,3,5,2,0]])
solve(a)
