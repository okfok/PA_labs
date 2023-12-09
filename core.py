import copy
import random
from copy import deepcopy

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab

GRAPH_SIZE = 150
EDGE_PROBABILITY = 0.05

BEE_COUNT = 22
SCOUT_COUNT = 3

COLORS = [None, 'green', 'red', 'yellow', 'blue', 'purple', 'darkred', 'orange', 'lime', 'cyan', 'violet']


class Cell:
    def __init__(self, val: bool = 0):
        self.val = val

    def __repr__(self):
        return str(self.val)

    def __bool__(self):
        return bool(self.val)


class Graph:
    def __init__(self, vertex_count: int = GRAPH_SIZE, skip_rand_gen: bool = False):

        self.count = vertex_count

        if skip_rand_gen:
            return
        self._edge_table = [
            [Cell(random.randint(0, 99) < (EDGE_PROBABILITY * 100)) for _ in range(i)]
            for i in range(vertex_count)
        ]

        self.color_map = [0 for _ in range(vertex_count)]
        self.used_colors = set()
        self.visited = set()

    def print_table(self):
        print(*self._edge_table, sep='\n')

    def edges(self, vertex):
        res = []
        if vertex != 0:
            res += enumerate(self._edge_table[vertex])

        for i in range(vertex, self.count - 1):
            res.append((i + 1, self._edge_table[i + 1][vertex]))

        return res

    def adjacent_vertexes(self, vertex):
        return [vert for vert, val in self.edges(vertex) if val]

    def adjacent_vertexes_colors(self, vertex):
        return set([self.color_map[vert] for vert in self.adjacent_vertexes(vertex)])

    def power_of_vertex(self, vertex):
        return sum(map(lambda x: x[1].val, self.edges(vertex)))

    def draw(self):
        visual = []

        for i in range(self.count):
            for j in range(i):
                if self._edge_table[i][j].val:
                    visual.append([i, j])
        G = nx.Graph()
        G.add_nodes_from([i for i in range(self.count)])

        G.add_edges_from(visual)
        plt.figure(figsize=(32, 24))
        # plt.axis = False
        color_map = [COLORS[i] for i in self.color_map]
        nx.draw_networkx(G, node_color=color_map, with_labels=True)
        plt.show()

    @property
    def chromatic_number(self):
        used_colors = set()
        for i in range(self.count):
            used_colors.add(self.color_map[i])

        return len(used_colors)

    def color_graph(self):
        while not all(self.color_map):
            pop = [i for i in range(self.count) if i not in self.visited]
            taken_vertexes = random.sample(pop, SCOUT_COUNT) if len(pop) > SCOUT_COUNT else pop
            nectar = [self.power_of_vertex(i) for i in taken_vertexes]
            if sum(nectar) == 0:
                self.color_vertex(random.choice(taken_vertexes))
                continue
            to_visit = random.choices(taken_vertexes, nectar)[0]
            self.visited.add(to_visit)

            self.color_vertex(to_visit)

    def color_vertex(self, vertex):
        self.color_map[vertex] = 0
        if self.power_of_vertex(vertex) == 0:
            self.color_map[vertex] = 1
            self.used_colors.add(1)
        else:
            adjacent = self.adjacent_vertexes(vertex)
            if BEE_COUNT < len(adjacent):
                nxt = random.sample(adjacent, BEE_COUNT)
            else:
                nxt = adjacent

            for nvert in nxt:
                for color in range(1, self.count):
                    if color not in self.adjacent_vertexes_colors(nvert):
                        self.used_colors.add(color)
                        self.color_map[nvert] = color
                        break
            for color in range(1, self.count):
                if color not in self.adjacent_vertexes_colors(vertex):
                    self.used_colors.add(color)
                    self.color_map[vertex] = color
                    break

    def improve_coloring(self, iteration_count: int):
        self.visited = set()
        for _ in range(iteration_count):
            vertexes = [i for i in range(self.count) if i not in self.visited]
            nectar = [self.power_of_vertex(i) for i in vertexes]
            if len(vertexes) == 0:
                return
            if sum(nectar) == 0:
                visited = random.choice(vertexes)
            else:
                visited = random.choices(vertexes, nectar)[0]
            self.color_vertex(visited)
            self.visited.add(visited)

    def copy(self):
        new = Graph(self.count)
        new._edge_table = copy.deepcopy(self._edge_table)
        new.color_map = copy.deepcopy(self.color_map)

        return new


def _main():
    g = Graph()
    g.color_graph()
    print('Chromatic number: ', last := g.chromatic_number)
    g.draw()
    states = []
    for _ in range(20):
        states.append(g)
        if last < g.chromatic_number:
            for state in reversed(states):
                if state.chromatic_number <= last:
                    g = state.copy()
        else:
            g = g.copy()
        g.improve_coloring(10)
        print('Chromatic number: ', g.chromatic_number)
        g.draw()


if __name__ == '__main__':
    _main()
