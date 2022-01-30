# Advanced Algorithms Homework 0
# Simplex Implementation
# Sam Coleman

def simplex(c, A, b):
    # Driver simplex function
    tableau = initialTableau(c, A, b)

    while canImprove(tableau):
        pivot = findPivotIndex(tableau)
        pivotAbout(tableau, pivot)
    
    return primalSolution(tableau), objectiveValue(tableau)

def initialTableau(c, A, b):
    # Make the initial augmented matrix
    tableau = [row[:] + [x] for row, x in zip(A, b)]
    tableau.append(c[:] + [0])
    return tableau

def canImprove(tableau):
    # Check if we are done (no more positive numbers in bottom row)
    last_row = tableau[-1]
    for num in last_row:
        if num > 0:
            return True
    
def findPivotIndex(tableau):
    # Pick first nonzero index of the last row
    for ind in range(0, len(tableau) - 1): 
        # Iterate through last row, except last element
        if tableau[-1][ind] > 0:
            column = ind
            break
    
    # Pivot math
    quotients = []
    for i,r in enumerate(tableau[:-1]):
        if r[column] > 0:
            quotients.append([i, r[-1] / r[column]])

    # Pivot value in row minimizing the quotient
    row = min(quotients, key=lambda x: x[1])[0]
    return row, column

def pivotAbout(tableau, pivot):
    # Use the pivot to clear the pivot column

    row, col = pivot
    pivot_denom = tableau[row][col]
    tableau[row] = [el / pivot_denom for el in tableau[row]]

    # Do the row operations
    for k,r in enumerate(tableau):
        if k != row:
            pivot_row_multiple = [el * tableau[k][col] for el in tableau[row]]
            tableau[k] = [x - y for x,y in zip(tableau[k], pivot_row_multiple)]

def primalSolution(tableau):
    # Value in last column, all rows except last row
    soln = []
    for i in range(0, len(tableau) - 1):
        soln.append(tableau[i][-1])
    
    return soln

def objectiveValue(tableau):
    # Value in bottom right corner (last column, last row)
    print(tableau)
    return -(tableau[-1][-1])

# c = [3, 2]
# A = [[1, 2, 1, 0], [1, -1, 0, 1]]
# b = [4, 1]

c = [6, 8, 0, 0]
A = [[5, 10, 1, 0], [4, 4, 0, 1]]
b = [60, 40]

c = [8, -6, 4, 0, 0, 0]
A = [[1, 1, 1, 1, 0, 0],
    [5, 3, 0, 0, 1, 0],
    [0, 9, 1, 0, 0, 1]]
b = [12, 20, 15]
print(simplex(c, A, b))
# column = [i for i,x in enumerate(a[-1][:-1]) if x > 0][0]
# print(a[:-1])
# for i, r in enumerate(a[:-1]):
#     print(i, r)
print(initialTableau(c, A, b))