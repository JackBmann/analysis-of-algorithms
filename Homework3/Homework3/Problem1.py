# Analysis of Algorithms Homework 3 Problem 1
# Jack Baumann 11/30/17

from random import randint



# Part A
# Generate 100 random points (x, y) where 0 <= x, y <= 100 and write them to random2DPoints.txt
with open('random2DPoints.txt', 'w') as file:
    for i in range(1, 101):
        x = randint(0, 100)
        y = randint(0, 100)
        file.write("p" + str(i) + ":(" + str(x) + "," + str(y) + ")\n")



# Part B
# Read the data in random2DPoints.txt and store it as fileData
with open('random2DPoints.txt', 'r') as file:
    fileData = file.read().split()

# Parse points from each line of fileData and append them to the list points
points = []
for line in fileData:
    pt = line.split("(")[1].split(",")
    x = int(pt[0])
    y = int(pt[1][:-1])
    points.append((x, y))

# Find the point with the lowest y coordinate, in case of a tie choose the point with the left-most x coordinate
p0 = points[0]
for p in points:
    if p[1] < p0[1]:
        p0 = p
    elif p[1] == p0[1] and p[0] < p0[0]:
        p0 = p


# Finds the angle of a given point from the bottom-most point, p0
def anglefromp0(u):
    if(p0[1] == u[1]):
        return 0
    return - (u[0] - p0[0]) / (u[1] - p0[1])


# Sort the points based on their angle from p0
points.remove(p0)
sortedPoints = sorted(points, key=anglefromp0)

# Create a stack to process the convex hole with
stack = []
stack.append(p0)
stack.append(sortedPoints[0])
stack.append(sortedPoints[1])


# Returns the angle formed between the line segments p0-p1 and p1-p2, if the angle is < 0, the turn is counter-clockwise
def checkForCounterClockwiseTurn(one, two, three):
    return (two[0] - one[0]) * (three[1] - one[1]) - (three[0] - one[0]) * (two[1] - one[1])


# Do the Graham scan to find the convex hull, which will be stored in the stack
m = len(points)
for i in range(2, m):
    while checkForCounterClockwiseTurn(stack[len(stack)-2], stack[len(stack)-1], sortedPoints[i]) <= 0:
        stack.pop()
    stack.append(sortedPoints[i])

print("1B Convex Hull: ", stack)



# Part C
# Read the data in random2DPoints.txt and store it as fileData
with open('random2DPoints.txt', 'r') as file:
    fileData = file.read().split()

# Parse points from each line of fileData and append them to the list points
unvistedPoints = []
for line in fileData:
    pt = line.split("(")[1].split(",")
    x = int(pt[0])
    y = int(pt[1][:-1])
    unvistedPoints.append((x, y))

# While there are still points that have not been used to create a line segment, select two random different points, create a line segment between them, and add them to lineSegments
lineSegments = []
n = len(unvistedPoints)
while n != 0:
    a = unvistedPoints[randint(0, n-1)]
    unvistedPoints.remove(a)
    b = unvistedPoints[randint(0, n-2)]
    unvistedPoints.remove(b)
    n -= 2
    lineSegments.append((a, b))



# Part D
# Computes the relative orientations of the points using their cross product
def direction(pi, pj, pk):
    # (pk - pi) x (pj - pi)
    return (pk[0] - pi[0]) * (pj[1] - pi[1]) - (pj[0] - pi[0]) * (pk[1] - pi[1])


# Determines if a point, pk, known to be colinear with a segment lies on that segment.
def onSegment(pi, pj, pk):
    if (min(pi[0], pj[0]) < pk[0] < max(pi[0], pj[0])) and (min(pi[1], pj[1]) < pk[1] < max(pi[1], pj[1])):
        return True
    return False


visitedLineSegments = []
intersectingLineSegments = []
# Go through every combination of line segments and check to see if they are intersecting
for seg1 in lineSegments:
    for seg2 in lineSegments:
        # If the line segment was already visited in the opposite order, continue
        if (seg2, seg1) in visitedLineSegments:
            continue
        
        p1 = seg1[0]
        p2 = seg1[1]
        p3 = seg2[0]
        p4 = seg2[1]

        # Compute the relative orientation of each endpoint with respect to the other line segment
        d1 = direction(p3, p4, p1)
        d2 = direction(p3, p4, p2)
        d3 = direction(p1, p2, p3)
        d4 = direction(p1, p2, p4)

        # If all the relative orientations are non-zero and the directions of the two points in each line segment are opposite then the lines cross each other
        if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
            intersectingLineSegments.append((seg1, seg2))

        # If any relative orientation is 0, then the point is colinear with the other segment, check if it is on the line segment
        elif(d1 == 0) and (onSegment(p3, p4, p1)):
            intersectingLineSegments.append((seg1, seg2))
        elif(d2 == 0) and (onSegment(p3, p4, p2)):
            intersectingLineSegments.append((seg1, seg2))
        elif(d3 == 0) and (onSegment(p1, p2, p3)):
            intersectingLineSegments.append((seg1, seg2))
        elif(d4 == 0) and (onSegment(p1, p2, p4)):
            intersectingLineSegments.append((seg1, seg2))

        # Hash the line segment as visited
        visitedLineSegments.append((seg1, seg2))

print("1C Random Line Segments formed between the random points: ", lineSegments)
print("1D The line segments that intersect each other: ", intersectingLineSegments)



# Part E
print("1E To determine if a point lies inside or outside of a polygon you could create a line segment between the point to test and a point that is known to be inside the polygon and test whether that line segment intersects with any of the line segments formed by the convex hull.")
