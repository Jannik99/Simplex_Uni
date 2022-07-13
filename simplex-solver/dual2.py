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
import time

np.set_printoptions(edgeitems=30, linewidth=100000, suppress=True)



def init(matrix):
    # Zielfunktion * -1 weil Minimierung
    num_rows, num_cols = matrix.shape
    print(f'Matrix {matrix}')
    matrix = np.multiply(matrix, -1)
    #matrix[np.delete(np.arange(matrix.shape[0]), num_rows - 1), :] *= -1
    print(f'Nach Multiplikation: \n {matrix}')
    #matrix = np.append(matrix, [np.zeros(matrix.shape[1])], axis=0)
    #print(f'Nach Z Reihe einsetzung: \n {matrix}')
    return matrix

def pivot(matrix):
    #print(f'Pivoting with: \n {matrix}')
    matrix.astype(np.longdouble)
    b_spalte = matrix[:-1, -1].astype(np.longdouble)
    c_reihe = matrix[-1, :].astype(np.longdouble)
    index_smallest_element = np.argmin(b_spalte)
    pivot_row = matrix[index_smallest_element, :].astype(np.longdouble)
    #print(f'Pivotreihe: {pivot_row}')
    print(f'Kleinstes Element an Position {index_smallest_element} ist: {b_spalte[index_smallest_element]}')
    #print(f'Zielfunktionsreihe: {c_reihe}')
    #print(f'Pivot_reihe: {pivot_row}')
    # # tmp = np.divide(c_reihe, pivot_row, where=pivot_row < 0)
    # #tmp = np.divide(c_reihe, pivot_row).astype(np.longdouble)
    # print(f'Temp Ergebnis: {tmp}')
    # # MUSS KLEINER NULL ABER DER GRÖßte sein
    # #tmp = tmp[np.where(np.sign(tmp) == -1)]
    # print(f'tmp: {tmp}')
    # tmp = tmp[np.less_equal(tmp, 0)]
    # print(f'tmp: {tmp}')
    tmp = np.subtract(z_reihe, c_reihe).astype(np.longdouble)
    #ratio = np.zeros(tmp.shape[0])
    ratio = []
    for x in range(0, tmp.size - 1):
        #print(f'Teile {tmp[x]} durch {pivot_row[x]}')
        if(pivot_row[x] != 0 and tmp[x] != 0):
            ratio.append(np.divide(tmp[x], pivot_row[x], dtype=np.longdouble))
    ratio = np.asarray(ratio, dtype=np.longdouble)    

    #np.true_divide(tmp, pivot_row, where=np.not_equal(pivot_row, 0), out=ratio ,dtype=np.longdouble).astype(np.longdouble)
    # in der ratio spalte sind werte aus 0/0 enthalten, welche numpy zu 0 evaluiert
    print(f'ratio: {ratio}')
    
    ratio = ratio[np.less_equal(ratio, 0)].astype(np.longdouble)
    index_largest_element = np.argmax(ratio[:-1])
    print(f'Größtes Element in der Tempspalte an Position {index_largest_element} ist: {ratio[index_largest_element]}')
    pivot_column = matrix[:, index_largest_element]
    #print(f'Pivotspalte: {pivot_column}')
    pivot_element = matrix[index_smallest_element, index_largest_element]
    print(f'Pivotelement: {pivot_element}')

    matrix[index_smallest_element, index_largest_element] = np.reciprocal(pivot_element)
    #print(f'1. Schritt: Kehrwert vom Pivotelement \n {matrix}')
    print(f'{matrix[index_smallest_element, index_largest_element]}')

    # Berechnung läuft falsch irgendwie

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
            else:
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
        print(f'\n Zielfunktionswert: {new_matrix[-1, -1] * -1}')
        finished = True if np.min(last_column_without_solution) >= 0 else False
        time.sleep(2)

a = np.array([[1,1,1,4,5,5], [4,1,4,3,3,9], [5,1,1,4,4,15], [1,3,3,5,2,0]]).astype(float)
#b = np.array([[4,5,4,1,5,2,7,2,9,22], [9,3,8,5,4,1,8,2,2,55], [4,8,1,7,8,6,6,3,9,24], [8,8,6,6,4,4,9,2,5,46], [4,2,3,1,5,9,6,4,4,6], [9,3,2,8,1,3,7,7,5,11], [7,8,3,5,3,1,3,6,8,59], [9,4,6,4,1,3,3,8,7,17], [9,5,3,8,6,8,5,3,1, 0]]).astype(float)
b = np.array([[11,1,11,12,11,9,1,2,3,13,6,12,10,7,6,78], [1,8,1,3,15,9,5,3,7,9,1,8,11,6,15,144], [7,7,7,15,3,8,8,12,9,11,6,5,14,4,5,79], [11,9,2,8,6,7,2,12,10,15,1,11,2,15,12,25], [14,9,7,14,2,5,3,4,1,5,6,9,1,2,4,71], [9,6,1,6,2,11,7,13,8,9,7,14,8,10,9,27], [3,7,8,7,2,15,3,8,15,7,9,4,14,3,10,179], [12,3,6,11,4,10,1,13,1,12,7,9,9,9,4,97], [8,9,3,8,14,14,13,1,7,7,13,13,3,5,2,138], [1,6,1,13,14,8,15,1,8,14,6,7,2,7,4,0]]).astype(np.longdouble)
z_reihe = np.zeros(b.shape[1]).astype(np.longdouble)
start(b)

    

