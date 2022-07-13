# Zielfunktion * -1
# >= Contstraints * -1
# Tableau -> ZeilenAnzahl = Anzahl Variablen von Zielfunktion + b Spalte
# Anzahl Reihen = Anzahl Schlupfvariablen
# PivotZeile = Kleinsten Wert in b Spalte
# tmp = Zielfunktionszeile (Letzte) / Pivotzeile where pivotzeile < 0 
# Maximaler Wert -> Index Pivotspalte
# Pivotelement = Schnittpunkt
# Simplexschritt: PivotElement_new = 1/Pivotelement
# Pivotzeile = Pivotzeile / Pivotelement (ALT) -> komplette Zeile
# Pivotspalte = - Pivotspalte / Pivotelement -> komplette Spalte
# die anderen ELemente = Element - (Index_Pivot_spalte * Index_Pivot_Zeile) / Pivotelement 
# Vertausche BasisVariablen???

from parser import *
import numpy as np

def init(matrix):
    # Zielfunktion * -1 weil Minimierung
    #tmp = np.multiply(matrix[:-1, :], -1)
    num_rows, num_cols = matrix.shape
    matrix[np.delete(np.arange(matrix.shape[0]), num_rows - 1), :] *= -1
    print(f'Nach Multiplikation: \n {matrix}')
    return matrix

def pivot(matrix):
    np.round(matrix, decimals=15)
    print(f'Pivoting with: \n {matrix}')
    b_spalte = matrix[:-1, -1]
    c_reihe = matrix[-1, :]
    index_smallest_element = np.argmin(b_spalte)
    pivot_row = matrix[index_smallest_element, :]
    print(f'Pivotreihe: {pivot_row}')
    print(f'Kleinstes Element an Position {index_smallest_element} ist: {b_spalte[index_smallest_element]}')
    #print(f'Zielfunktionsreihe: {c_reihe}')
    tmp = np.divide(c_reihe, pivot_row, where=pivot_row < 0)
    print(f'Temp Ergebnis: {tmp[-1]}')
    index_largest_element = np.argmax(tmp[:-1])
    print(f'Größtes Element in der Tempspalte an Position {index_largest_element} ist: {tmp[index_largest_element]}')
    pivot_column = matrix[:, index_largest_element]
    print(f'Pivotspalte: {pivot_column}')
    pivot_element = matrix[index_smallest_element, index_largest_element]

    matrix[index_smallest_element, index_largest_element] = np.reciprocal(pivot_element)

    print(f'1. Schritt: Kehrwert vom Pivotelement \n {matrix}')

    pivot_position = (index_smallest_element, index_largest_element)
    with np.nditer(matrix, op_flags=['readwrite'], flags=['multi_index']) as iterator:
        new_pivot_row = []
        for x in iterator:
        # check if we are in pivot Row
            if iterator.multi_index[0] == pivot_position[0]:
                if iterator.multi_index != pivot_position:
                    new_pivot_row.append(x / pivot_element)
                else:
                    new_pivot_row.append(matrix[index_smallest_element, index_largest_element])
                    #print(f'Neu Zeile: {new_pivot_row}')
            elif iterator.multi_index[1] == pivot_position[1]:
                if iterator.multi_index != pivot_position:
                    new_pivot_column = np.divide(pivot_column, pivot_element) * -1
                    #x /= -pivot_element
            else:   #x = -3/2 - (-1/4/3)
                # x = -3/2 - (-1/12)
            # a10 = a10 - a1t * as0 / Pivot_element
            # a10 = -2 - (-1*-1)/-2
                if iterator.multi_index != pivot_position:
                    #print(f'Alles andere {iterator.multi_index}')
                    #pivot_row = matrix[index_smallest_element, :]
                    #pivot_column = matrix[:, index_largest_element]
                    x -= (pivot_row[iterator.multi_index[1]]*pivot_column[iterator.multi_index[0]])/pivot_element
    matrix[:, index_largest_element] = new_pivot_column
    print(f'Neue Pivot Reihe: {new_pivot_row}')
    matrix[index_smallest_element, :] = new_pivot_row            
    
    print(f'Matrix nach Simplex Schritt: \n {matrix}')
    return matrix

def start(parsed):
    new_matrix = init(parsed)
    iterations = 1
    finished = False
    while finished is False:
        new_matrix = pivot(new_matrix)
        iterations += 1
        last_column_without_solution = new_matrix[:, -1][:-1]
        print(f'\n Zielfunktionswert: {new_matrix[-1, -1]}')
        finished = True if np.min(last_column_without_solution) >= 0 else False

# f(x1,x2) = x1+x2 -> min
# x1 + 2x2 >= 6
# 2x1 + x2 >= 6
# NUR DER AUFGABE ZU SCHULDEN: x1+x2 = 4 -> KEINE VERGLEICHBARE CONSTRAINT IN BENCHMARKS
a = np.array([[1,2,6], [2,1,6], [-1,-1,-4], [1,1,4], [1,1,0]]).astype(float)
#b = np.array([[1,1,1,4,5,5], [4,1,4,3,3,9], [5,1,1,4,4,15], [1,3,3,5,2,0]]).astype(float)
#b = np.array([[4,5,4,1,5,2,7,2,9,22], [9,3,8,5,4,1,8,2,2,55], [4,8,1,7,8,6,6,3,9,24], [8,8,6,6,4,4,9,2,5,46], [4,2,3,1,5,9,6,4,4,6], [9,3,2,8,1,3,7,7,5,11], [7,8,3,5,3,1,3,6,8,59], [9,4,6,4,1,3,3,8,7,17], [9,5,3,8,6,8,5,3,1, 0]]).astype(float)
#b = np.array([[11,1,11,12,11,9,1,2,3,13,6,12,10,7,6,78], [1,8,1,3,15,9,5,3,7,9,1,8,11,6,15,144], [7,7,7,15,3,8,8,12,9,11,6,5,14,4,5,79], [11,9,2,8,6,7,2,12,10,15,1,11,2,15,12,25], [14,9,7,14,2,5,3,4,1,5,6,9,1,2,4,71], [9,6,1,6,2,11,7,13,8,9,7,14,8,10,9,27], [3,7,8,7,2,15,3,8,15,7,9,4,14,3,10,179], [12,3,6,11,4,10,1,13,1,12,7,9,9,9,4,97], [8,9,3,8,14,14,13,1,7,7,13,13,3,5,2,138], [1,6,1,13,14,8,15,1,8,14,6,7,2,7,4,0]]).astype(float)
#new_matrix = init(b)
parsed_benchmarks = getParsedBenchmarks()
benchmarks = []
for i, parsed in enumerate(parsed_benchmarks):
    benchmarks.append(parsed[0])

for benchmark in benchmarks:
    start(benchmark.astype(float))

    

