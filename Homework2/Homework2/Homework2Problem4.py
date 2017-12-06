from sys import stdin
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, NodePath
from math import floor
from libraries.scipy import misc

# Problem 4 Part A                                                                                      # Part B
print("Enter .bmp file path would you like to read: ")                                                  # c
filepath = stdin.readline().strip()                                                                     # c
I = misc.imread(filepath, flatten=True, mode='F')                                                       # n^2


def reduceOnce(G):                                                                                      # n + c
    print(str(len(G)) + "x" + str(len(G)) + " reduction: ")                                             # n
    newG = []                                                                                           # n
    for row in range(0, len(G), 2):                                                                     # n/2
        newRow = []                                                                                     # c
        for col in range(0, len(G[0]), 2):                                                              # n/2
            newRow.append((G[row][col] + G[row][col+1] + G[row+1][col] + G[row+1][col+1]) / 4.0)        # c
        newG.append(newRow)                                                                             # c
        print(newRow)                                                                                   # c
    return newG                                                                                         # c


def reduceToFinalLayer(G):                                                                              # (1/2)n^2 + cn + c
    if len(G) == 2:                                                                                     # c
        return reduceOnce(G)                                                                            # n+c
    return reduceToFinalLayer(reduceOnce(G))                                                            # (n/2)*(n+c)


def transformCurve(curve, x, y):                                                                        # n + c
    transformedCurve = []                                                                               # c
    for point in curve:                                                                                 # n
        transformedCurve.append([point[0] + x, 0, point[2] + y])                                        # c
    return transformedCurve                                                                             # c


def scaleCurve(curve, scale):                                                                           # n + c
    scaledCurve = []                                                                                    # c
    for point in curve:                                                                                 # n
        scaledCurve.append([point[0]/scale, 0, point[2]/scale])                                         # c
    return scaledCurve                                                                                  # c


def rotateCurveLeft(curve):                                                                             # 2n + c
    rotatedCurve = []                                                                                   # c
    for point in curve:                                                                                 # n
        rotatedCurve.append([-point[2], 0, point[0]])                                                   # c
    return rotatedCurve[::-1]                                                                           # n


def rotateCurveRight(curve):                                                                            # 2n + c
    rotatedCurve = []                                                                                   # c
    for point in curve:                                                                                 # n
        rotatedCurve.append([point[2], 0, -point[0]])                                                   # c
    return rotatedCurve[::-1]                                                                           # n


def generateHilbertCurveAtDepth(pts, d, scale):                                                         # 13n + d + c
    for i in range(1, d):                                                                               # d
        pts = generateSingleHilbertCurve(pts, scale)                                                    # 13n + c
    return pts                                                                                          # c


def generateSingleHilbertCurve(pts, scale):                                                             # 13n + c
    newCurve = []                                                                                       # c
    bottomLeftCurve = rotateCurveRight(transformCurve(scaleCurve(pts, scale), 0.5, -0.5))               # 4n + c
    topLeftCurve = transformCurve(scaleCurve(pts, scale), -0.5, 0.5)                                    # 2n + c
    topRightCurve = transformCurve(scaleCurve(pts, scale), 0.5, 0.5)                                    # 2n + c
    bottomRightCurve = rotateCurveLeft(transformCurve(scaleCurve(pts, scale), -0.5, -0.5))              # 4n + c
    for p in bottomLeftCurve:                                                                           # n/4
        newCurve.append(p)                                                                              # c
    for p in topLeftCurve:                                                                              # n/4
        newCurve.append(p)                                                                              # c
    for p in topRightCurve:                                                                             # n/4
        newCurve.append(p)                                                                              # c
    for p in bottomRightCurve:                                                                          # n/4
        newCurve.append(p)                                                                              # c
    return newCurve                                                                                     # c


def drawHilbertCurve(pts):                                                                              # 2n + c
    for p in range(len(pts) - 1):                                                                       # n
        seg = LineSegs()                                                                                # c
        seg.setThickness(3)                                                                             # c
        seg.draw_to(pts[p][0], 0, pts[p][2])                                                            # c
        seg.draw_to(pts[p+1][0], 0, pts[p+1][2])                                                        # c
        node = seg.create()                                                                             # c
        nodes.append(node)                                                                              # c

    for node in nodes:                                                                                  # n
        base.aspect2d.attach_new_node(node)                                                             # c


def getXTransformScale(x, s):                                                                           # c
    if x == 0:                                                                                          # c
        return -(x-1)/s                                                                                 # c
    elif x == s:                                                                                        # c
        return (x-1)/s                                                                                  # c
    elif x <= s/2:                                                                                      # c
        return -x/s + getXTransformScale(x, s/2)                                                        # c
    else:                                                                                               # c
        return (x-1)/s + getXTransformScale(s-x+1, s/2)                                                 # c


def getProperDepth(val):                                                                                # c
    if val >= 5:                                                                                        # c
        return 5                                                                                        # c
    if val <= 1:                                                                                        # c
        return 1                                                                                        # c
    return int(floor(val))                                                                              # c


def getQuadrantPoints(quadrantSize):                                                                    # 16n + d + c
    quadrantCurves = []                                                                                 # c
    for r in range(size):                                                                               # n
        rowCurves = []                                                                                  # c
        for c in range(size):                                                                           # n
            depth = getProperDepth(oneReductionLayer[r][c])                                             # c
            quadrantCurve = scaleCurve(generateHilbertCurveAtDepth(basePoints, depth, 2), quadrantSize)  # 14n + d + c
            rowCurves.append(quadrantCurve)                                                             # c
        quadrantCurves.append(rowCurves)                                                                # c
    return quadrantCurves                                                                               # c


def stitchCurvesTogether(bottomLeft, topLeft, topRight, bottomRight):                                   # 3n + c
    newCurve = bottomLeft                                                                               # c
    for p in topLeft:                                                                                   # n
        newCurve.append(p)                                                                              # c
    for p in topRight:                                                                                  # n
        newCurve.append(p)                                                                              # c
    for p in bottomRight:                                                                               # n
        newCurve.append(p)                                                                              # c
    return newCurve                                                                                     # c


def transformAndStitchCurves(points, size, x, y):                                                       # 7n + 4log(n) + c
    if size == 1:                                                                                       # c
        return points                                                                                   # c
    else:                                                                                               # c
        bottomLeft = transformCurve(transformAndStitchCurves(points[0], size/2, x, y), x, y)            # n + log(n)
        topLeft = transformCurve(transformAndStitchCurves(points[1], size/2, x, y+0.5), x, y+0.5)       # n + log(n)
        topRight = transformCurve(transformAndStitchCurves(points[2], size/2, x+0.5, y+0.5), x+0.5, y+0.5)  # n + log(n)
        bottomRight = transformCurve(transformAndStitchCurves(points[3], size/2, x+0.5, y), x+0.5, y)   # n + log(n)
        stitchedTogether = stitchCurvesTogether(bottomLeft, topLeft, topRight, bottomRight)             # 3n + c
        return stitchedTogether                                                                         # c


oneReductionLayer = reduceOnce(I)                                                                       # n + c
pyramidRoot = reduceToFinalLayer(I)                                                                     # (1/2)n^2 + cn + c
basePoints = [[-0.5, 0, -0.5], [-0.5, 0, 0.5], [0.5, 0, 0.5], [0.5, 0, -0.5]]                           # c
nodes = []                                                                                              # c
finalPoints = []                                                                                        # c
base = ShowBase()                                                                                       # c
size = len(oneReductionLayer)                                                                           # c
quadrantPoints = getQuadrantPoints(size)                                                                # 16n + d + c
stitchedTogether = transformAndStitchCurves(quadrantPoints, size, -0.4, -0.4)                           # 7n + 4log(n) + c
for point in stitchedTogether:                                                                          # n
    finalPoints.append(point)                                                                           # c
drawHilbertCurve(finalPoints)                                                                           # C
base.run()                                                                                              # c

# Total computational cost: (3/2)n^2 + 25n + 4log(n) + d + c
