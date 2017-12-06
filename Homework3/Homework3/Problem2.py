# Analysis of Algorithms Homework 3 Problem 2
# Jack Baumann 12/1/17

from random import randint
from queue import PriorityQueue



# Part A
# I unfortunately could not come up with a good way to generate a random graph
G = {'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['A', 'B']}




# Part B
# Initializes each vertex in the graph
def initializeSingleSource(G, s):
    for vertex in G.keys():
        vertex.distance = sys.maxsize
        vertex.parent = None
    s.distance = 0


# Check if the shortest path to v found so far by going through u can be improved and if so update its distance an parent
def relax(u, v, w):
    if v.distance > u.distance + w(u, v):
        v.distance = u.distance + w(u, v)
        v.parent = u


# Find the single source shortest path using Dijkstra's algorithm
initializeSingleSource(G, 'A')
S = []
Q = PriorityQueue
for v in G.keys():
    Q.put(v)
while Q.not_empty:
    u = Q.get()
    S.append(u)
    for vertex in G[u]:
        relax(u, v, w)
