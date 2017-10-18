import csv
from sys import stdin

# Problem 2 Part A
# print "Enter .csv file path would you like to read: "
# filepath = stdin.readline().strip()

I = []
# with open(filepath) as csvfile:
with open('homework2.csv') as csvfile:
    data = csv.reader(csvfile)
    print "Imputed data: "
    for line in data:
        l = map(float, line)
        print l
        I.append(l)


# Problem 2 Part B                                                                                      Part C
def reduceOnce(G):                                                                                      # n+c
    print str(len(G)) + "x" + str(len(G)) + " reduction: "
    newG = []
    for row in range(0, len(G), 2):                                                                     # n/2
        newRow = []                                                                                     # c
        for col in range(0, len(G[0]), 2):                                                              # n/2
            newRow.append((G[row][col] + G[row][col+1] + G[row+1][col] + G[row+1][col+1]) / 4.0)        # c
        newG.append(newRow)                                                                             # c
        print newRow
    return newG                                                                                         # c


def reduceToFinalLayer(G):                                                                              # n^2 + c
    if len(G) == 2:                                                                                     # c
        return reduceOnce(G)                                                                            # n+c
    return reduceToFinalLayer(reduceOnce(G))                                                            # (n/2)*(n+c)

reduceToFinalLayer(I)
