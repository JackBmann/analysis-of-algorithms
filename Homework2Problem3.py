from sys import stdin
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, NodePath
import csv
from math import floor

# Problem 3 Part A
# print("Enter .csv file path would you like to read: ")
# filepath = stdin.readline().strip()
filepath = "homework2.csv"

I = []
with open(filepath) as csvfile:
    data = csv.reader(csvfile)
    print("Imputed data: ")
    for line in data:
        l = map(float, line)
        print(l)
        I.append(l)

def reduceOnce(G):
    print(str(len(G)) + "x" + str(len(G)) + " reduction: ")
    newG = []
    for row in range(0, len(G), 2):
        newRow = []
        for col in range(0, len(G[0]), 2):
            newRow.append((G[row][col] + G[row][col+1] + G[row+1][col] + G[row+1][col+1]) / 4.0)
        newG.append(newRow)
        print(newRow)
    return newG

def reduceToFinalLayer(G):
    if len(G) == 2:
        return reduceOnce(G)
    return reduceToFinalLayer(reduceOnce(G))

oneReductionLayer = reduceOnce(I)
pyramidRoot = reduceToFinalLayer(I)
basePoints = [[-0.5, 0, -0.5], [-0.5, 0, 0.5], [0.5, 0, 0.5], [0.5, 0, -0.5]]
nodes = []
base = ShowBase()

def transformCurve(curve, x, y):
    transformedCurve = []
    for point in curve:
        transformedCurve.append([point[0] + x, 0, point[2] + y])
    return transformedCurve

def scaleCurve(curve, scale):
    scaledCurve = []
    for point in curve:
        scaledCurve.append([point[0]/scale, 0, point[2]/scale])
    return scaledCurve

def rotateCurveLeft(curve):
    rotatedCurve = []
    for point in curve:
        rotatedCurve.append([-point[2], 0, point[0]])
    return rotatedCurve[::-1]

def rotateCurveRight(curve):
    rotatedCurve = []
    for point in curve:
        rotatedCurve.append([point[2], 0, -point[0]])
    return rotatedCurve[::-1]

def generateHilbertCurveAtDepth(pts, d, scale):
    for i in range(1, d):
        pts = generateSingleHilbertCurve(pts, scale)
    return pts

def generateSingleHilbertCurve(pts, scale):
    newCurve = []
    bottomLeftCurve = rotateCurveRight(transformCurve(scaleCurve(pts, scale), 0.5, -0.5))
    topLeftCurve = transformCurve(scaleCurve(pts, scale), -0.5, 0.5)
    topRightCurve = transformCurve(scaleCurve(pts, scale), 0.5, 0.5)
    bottomRightCurve = rotateCurveLeft(transformCurve(scaleCurve(pts, scale), -0.5, -0.5))
    for p in bottomLeftCurve:
        newCurve.append(p)
    for p in topLeftCurve:
        newCurve.append(p)
    for p in topRightCurve:
        newCurve.append(p)
    for p in bottomRightCurve:
        newCurve.append(p)
    return newCurve

def drawHilbertCurve(pts):
    for p in range(len(pts) - 1):
        seg = LineSegs()
        seg.setThickness(3)
        seg.draw_to(pts[p][0], 0, pts[p][2])
        seg.draw_to(pts[p+1][0], 0, pts[p+1][2])
        node = seg.create()
        nodes.append(node)

    for node in nodes:
        base.aspect2d.attach_new_node(node)

def getTransformScale(n, s):
    if n+1 <= s/2:
        return -n/s - (n+1)/s
    else:
        return n/s

def getProperDepth(val):
    if val >= 5:
        return 5
    if val <= 1:
        return 1
    return int(floor(val))

points = []
size = len(oneReductionLayer)
sizeScale = size
for row in range(size):
    for col in range(size):
        depth = getProperDepth(oneReductionLayer[row][col])
        # sizeScale = float(depth)
        xTransformScale = getTransformScale(row, float(size))
        yTransformScale = getTransformScale(col, float(size))
        sectionCurve = transformCurve(scaleCurve(generateHilbertCurveAtDepth(basePoints, depth, sizeScale),
                                                 sizeScale), xTransformScale, yTransformScale)
        for point in sectionCurve:
            points.append(point)

drawHilbertCurve(points)
base.run()
