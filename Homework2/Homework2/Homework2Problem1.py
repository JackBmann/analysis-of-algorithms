from sys import stdin
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, NodePath

# Problem 1 Part A                                                                                  # Part B
print("Enter the depth of the Hilbert Curve: ")                                                     # c
d = int(stdin.readline().strip())                                                                   # c

points = [[-0.5, 0, -0.5], [-0.5, 0, 0.5], [0.5, 0, 0.5], [0.5, 0, -0.5]]                           # c
nodes = []                                                                                          # c
base = ShowBase()                                                                                   # c


def transformCurve(curve, x, y):                                                                    # n + c
    transformedCurve = []                                                                           # c
    for point in curve:                                                                             # n
        transformedCurve.append([point[0]/2 + x, 0, point[2]/2 + y])                                # c
    return transformedCurve                                                                         # c


def scaleCurve(curve, x, y):                                                                        # n + c
    scaledCurve = []                                                                                # c
    for point in curve:                                                                             # n
        scaledCurve.append([point[0]/2, 0, point[2]/2])                                             # c
    return scaledCurve                                                                              # c


def rotateCurveLeft(curve):                                                                         # 2n + c
    rotatedCurve = []                                                                               # c
    for point in curve:                                                                             # n
        rotatedCurve.append([-point[2], 0, point[0]])                                               # c
    return rotatedCurve[::-1]                                                                       # n


def rotateCurveRight(curve):                                                                        # 2n + c
    rotatedCurve = []                                                                               # c
    for point in curve:                                                                             # n
        rotatedCurve.append([point[2], 0, -point[0]])                                               # c
    return rotatedCurve[::-1]                                                                       # n


for i in range(1, d):                                                                               # d(12n) + c
    newCurve = []                                                                                   # c
    bottomLeftCurve = rotateCurveRight(transformCurve(points, 0.5, -0.5))                           # (2n+c)+(n+c) + c
    topLeftCurve = transformCurve(points, -0.5, 0.5)                                                # n + c
    topRightCurve = transformCurve(points, 0.5, 0.5)                                                # n + c
    bottomRightCurve = rotateCurveLeft(transformCurve(points, -0.5, -0.5))                          # (2n+c)+(n+c) + c
    for p in bottomLeftCurve:                                                                       # n
        newCurve.append(p)                                                                          # c
    for p in topLeftCurve:                                                                          # n
        newCurve.append(p)                                                                          # c
    for p in topRightCurve:                                                                         # n
        newCurve.append(p)                                                                          # c
    for p in bottomRightCurve:                                                                      # n
        newCurve.append(p)                                                                          # c
    points = newCurve                                                                               # c

for p in range(len(points) - 1):                                                                    # n
    seg = LineSegs()                                                                                # c
    seg.setThickness(3)                                                                             # c
    seg.draw_to(points[p][0], 0, points[p][2])                                                      # c
    seg.draw_to(points[p+1][0], 0, points[p+1][2])                                                  # c
    node = seg.create()                                                                             # c
    nodes.append(node)                                                                              # c

for node in nodes:                                                                                  # n
    base.aspect2d.attach_new_node(node)                                                             # c

base.run()                                                                                          # c

# Total computational cost: d(12n) + 2n + c
