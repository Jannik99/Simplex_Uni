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
    # copy transposed matrix into new big matrix
    new_matrix[:, 0:num_cols - 1] = transposed[:, 0:num_cols - 1]
    # access last column of new matrix and paste last column from transposed matrix
    new_matrix[:, -1] = transposed[:, -1]

    pivot_element = search_pivot(new_matrix)
    # TODO: Schlupfvariablen müssen noch mit 1 gefüllt werden
    print(new_matrix)
    print(pivot_element)

def search_pivot(matrix):
    last_row = matrix[len(matrix)-1 , :-1]
    # find position of largest element in last row
    index_largest_element = np.argmax(last_row, axis = 0)
    pivot_column = matrix[:-1, index_largest_element]

    # take last columns and divide it with pivot column
    last_column = matrix[:-1, -1]
    tmp = last_column / pivot_column
    # find position of smallest element in temporary column
    index_smallest_element = np.argmin(tmp, axis = 0)

    # find pivot element with intersection point which has been calculated
    pivot_element = matrix[index_smallest_element, index_largest_element]
    
    return pivot_element
    
a = np.array([[1,1,1,4,5,5], [4,1,4,3,3,9], [5,1,1,4,4,15], [1,3,3,5,2,0]])
solve(a)
