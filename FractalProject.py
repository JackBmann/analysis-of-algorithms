# Fractal Project - Jack Baumann - Oct. 7, 2017
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, NodePath
from math import sqrt


def draw_triangle(triangle, color):
    point1 = triangle[0]
    point2 = triangle[1]
    point3 = triangle[2]

    seg1 = LineSegs()
    seg1.setColor(color[0], color[1], color[2], 1)
    seg1.setThickness(3)
    seg1.draw_to(point1[0], 0, point1[1])  # x, z, y
    seg1.draw_to(point2[0], 0, point2[1])  # x, z, y
    node1 = seg1.create()
    nodes.append(node1)

    seg2 = LineSegs()
    seg2.setColor(color[0], color[1], color[2], 1)
    seg2.setThickness(3)
    seg2.draw_to(point2[0], 0, point2[1])  # x, z, y
    seg2.draw_to(point3[0], 0, point3[1])  # x, z, y
    node2 = seg2.create()
    nodes.append(node2)

    seg3 = LineSegs()
    seg3.setColor(color[0], color[1], color[2], 1)
    seg3.setThickness(3)
    seg3.draw_to(point3[0], 0, point3[1])  # x, z, y
    seg3.draw_to(point1[0], 0, point1[1])  # x, z, y
    node3 = seg3.create()
    nodes.append(node3)


def iterate(triangle, iteration_count):
    if iteration_count > 0:
        point1 = triangle[0]
        point2 = triangle[1]
        point3 = triangle[2]

        red_point1 = point1
        red_point2 = [point1[0] + (point2[0] - point1[0]) / 2.0, point2[1]]
        red_point3 = [point1[0] + (red_point2[0] - point1[0]) / 2.0, point1[1] + (point3[1] - point1[1]) / 2.0]
        red_triangle = [red_point1, red_point2, red_point3]
        draw_triangle(red_triangle, red)
        iterate(red_triangle, iteration_count - 1)

        green_point1 = [(point1[0] + point2[0]) / 2.0, point1[1]]
        green_point2 = point2
        green_point3 = [(green_point1[0] + point2[0]) / 2.0, point3[1] - (point3[1] - point1[1]) / 2.0]
        green_triangle = [green_point1, green_point2, green_point3]
        draw_triangle(green_triangle, green)
        iterate(green_triangle, iteration_count - 1)

        blue_point1 = [point1[0] + (point3[0] - point1[0]) / 2.0, point3[1] - (point3[1] - point1[1]) / 2.0]
        blue_point2 = [point3[0] + (point2[0] - point3[0]) / 2.0, point3[1] - (point3[1] - point1[1]) / 2.0]
        blue_point3 = point3
        blue_triangle = [blue_point1, blue_point2, blue_point3]
        draw_triangle(blue_triangle, blue)
        iterate(blue_triangle, iteration_count - 1)

    else:
        return


base = ShowBase()
nodes = []
iterations = 9
pointA = [-0.5 * sqrt(3), -0.75]
pointB = [0.5 * sqrt(3), -0.75]
pointC = [0, 0.75]
base_triangle = [pointA, pointB, pointC]
red = [1, 0, 0]
green = [0, 1, 0]
blue = [0, 0, 1]
iterate(base_triangle, iterations)

for node in nodes:
    base.aspect2d.attach_new_node(node)

base.run()
