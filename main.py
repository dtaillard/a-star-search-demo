#!/usr/bin/env python3

import graph as gh

from heapq import *
from math import inf
from sys import argv
from time import time

def heuristic(node, goal):
    (x1, y1) = node
    (x2, y2) = goal
    
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    # Chebychev distance
    D = 1
    D2 = 1
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    # Manhattan distance
    #return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(start, goal, graph):
    frontier = []
    came_from = {}
    cost = {}

    heappush(frontier, (0, start))
    came_from[start] = None
    cost[start] = 0

    # should never happen if path to goal is possible
    if graph.is_obstacle(start):
        return None

    while frontier:
        current = heappop(frontier)[1]
        
        if current == goal:
            return came_from

        for neighbor in graph.neighbors(current):
            new_cost = cost[current] + graph.cost_to(current, neighbor) 

            if new_cost < cost.get(neighbor, inf) and not graph.is_obstacle(neighbor):
                cost[neighbor] = new_cost
                came_from[neighbor] = current
                priority = new_cost + heuristic(neighbor, goal)

                heappush(frontier, (priority, neighbor))
    return None

def reconstruct_path(start, goal, came_from):
    result = []
    node = goal
    while node != None:
        result.append(node)
        node = came_from[node]
    return result

def print_graph(path, graph):
    GREEN = '\033[38;5;82m'
    RED = '\033[38;5;196m'
    RESET = '\033[0m'

    for y in range(graph.height):
        for x in range(graph.width):
            node = (x, y)

            if graph.is_obstacle(node): c = RED + '= ' + RESET
            elif node in path: c = GREEN + '# ' + RESET
            else: c = '. '

            print(c, end='')
        print() # print newline

if __name__ == '__main__':
    if len(argv) > 1 and argv[1].isdigit():
        
        print('Using %s%% obstacle chance.' % argv[1])

        # change from percent
        obstacle_chance = float(argv[1]) / 100
    else:
        print('Defaulting to 20% obstacle chance.')
        obstacle_chance = 0.2

    graph = gh.RandomObstacleGraph(32, 32, obstacle_chance)

    start = (0, 0)  # upper left corner
    goal = (31, 31) # lower right corner

    print('Calculating path...')

    last_time = time()
    came_from = a_star_search(start, goal, graph)

    if came_from != None:
        path = reconstruct_path(start, goal, came_from) 
        print_graph(path, graph)
    else:
        print('No path was found.')

    print('Finished in %fs.' % (time() - last_time))
