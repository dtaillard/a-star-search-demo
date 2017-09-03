from abc import ABC, abstractmethod
from random import random

class Graph(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    @abstractmethod
    def is_obstacle(self, node):
        pass

    @abstractmethod
    def cost_to(self, from_node, to_node):
        pass

    def exists_node(self, node):
        (x, y) = node
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, node):
        (x, y) = node
        result = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), \
                (x - 1, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1)]

        return filter(self.exists_node, result)

    def heuristic(self, node, goal):
        (x1, y1) = node
        (x2, y2) = goal
    
        # Manhattan distance
        #return abs(x1 - x2) + abs(y1 - y2)

        # Chebychev distance
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)

        D = D2 = 1
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

class RandomObstacleGraph(Graph):
    def __init__(self, width, height, obstacle_chance):
        super().__init__(width, height)

        self.obstacles = []

        for y in range(height):
            for x in range(width):
                if random() < obstacle_chance:
                    self.obstacles.append((x, y))

    def is_obstacle(self, node):
        return node in self.obstacles

    def cost_to(self, from_node, to_node):
        return 1 # all nodes in this Graph class have a weight of 1

class PredefinedGraph(Graph):
    def __init__(self, width, height, nodes_dict):
        super().__init__(width, height)

        self.nodes_dict = nodes_dict

    def is_obstacle(self, node):
        # -1 weights represent obstacles
        return nodes[node] == -1

    def cost_to(self, from_node, to_node):
        return nodes[node]
