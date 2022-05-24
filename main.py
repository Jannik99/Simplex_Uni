# A Function taking variables and running a simplex algorithm with recursion
def simplex(c, A, b, m):
    # Initialize the variables
    n = len(c)
    x = [0] * n
    # Run the simplex algorithm
    while True:
        # Check if the solution is optimal
        if check_optimal(c, A, b, x):
            return x
        # Find the pivot
        pivot = find_pivot(c, A, b, x)  
        # Check if the solution is unbounded
        if pivot == None:
            return None
        # Perform the pivot
        pivot_row = A[pivot]
        pivot_value = pivot_row[pivot]
        for i in range(n):
            pivot_row[i] /= pivot_value
        b[pivot] /= pivot_value
        for i in range(m):
            if i != pivot:
                row = A[i]
                factor = row[pivot]
                for j in range(n):
                    row[j] -= factor * pivot_row[j]
                b[i] -= factor * b[pivot]
        # Update the solution
        x[pivot] = 1
        for i in range(n):
            if i != pivot:
                x[i] = 0  
    # Return the solution
    return x
# A Function checking if the solution is optimal
def check_optimal(c, A, b, x):
    # Initialize the variables
    n = len(c)
    m = len(A)
    # Check if the solution is optimal  
    for i in range(n):
        if c[i] > 0 and x[i] < 0:
            return False
    for i in range(m):
        if b[i] < 0:
            return False
    return True
# A Function finding the pivot
def find_pivot(c, A, b, x):
    # Initialize the variables
    n = len(c)
    m = len(A)
    # Find the pivot
    for i in range(m):
        if b[i] < 0:
            return i
    for i in range(n):
        if c[i] > 0 and x[i] < 0:
            return i
    return None
# A Function printing the solution
def print_solution(x):
    # Initialize the variables
    n = len(x)
    # Print the solution
    for i in range(n):
        print("x" + str(i) + " = " + str(x[i]))


def main():
    # Initialize the variables
    c = [1, 1, 1]
    A = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    b = [1, 1, 1]
    m = len(A)
    # Run the simplex algorithm
    x = simplex(c, A, b, m)
    # Print the solution
    print_solution(x)
    