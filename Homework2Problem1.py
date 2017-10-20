from sys import stdin
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, NodePath

# Problem 1 Part A
print("Enter the depth of the Hilbert Curve: ")
d = int(stdin.readline().strip())

points = [[-0.5, 0, -0.5], [-0.5, 0, 0.5], [0.5, 0, 0.5], [0.5, 0, -0.5]]
nodes = []
base = ShowBase()

def transformCurve(curve, x, y):
    transformedCurve = []
    for point in curve:
        transformedCurve.append([point[0]/2 + x, 0, point[2]/2 + y])
    return transformedCurve

def scaleCurve(curve, x, y):
    scaledCurve = []
    for point in curve:
        scaledCurve.append([point[0]/2, 0, point[2]/2])
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


for i in range(1, d):
    newCurve = []
    bottomLeftCurve = rotateCurveRight(transformCurve(points, 0.5, -0.5))
    topLeftCurve = transformCurve(points, -0.5, 0.5)
    topRightCurve = transformCurve(points, 0.5, 0.5)
    bottomRightCurve = rotateCurveLeft(transformCurve(points, -0.5, -0.5))
    for p in bottomLeftCurve:
        newCurve.append(p)
    for p in topLeftCurve:
        newCurve.append(p)
    for p in topRightCurve:
        newCurve.append(p)
    for p in bottomRightCurve:
        newCurve.append(p)
    points = newCurve

for p in range(len(points) - 1):
    seg = LineSegs()
    seg.setThickness(3)
    seg.draw_to(points[p][0], 0, points[p][2])
    seg.draw_to(points[p+1][0], 0, points[p+1][2])
    node = seg.create()
    nodes.append(node)

for node in nodes:
    base.aspect2d.attach_new_node(node)

base.run()
