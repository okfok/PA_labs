import random

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

GRAPH_SIZE = 300
EDGE_PROBABILITY = 0.05

POPULATION_SIZE = 10
MUTATION_PROBABILITY = 0.025


class Solution:
    def __init__(self, graph=None, genes=None):
        self.graph = graph or nx.gnp_random_graph(GRAPH_SIZE, EDGE_PROBABILITY)
        self.genes = genes or [False for _ in range(GRAPH_SIZE)]

    @property
    def cover_len(self):
        return sum(self.genes)

    def __repr__(self):
        return f'Sol({self.cover_len})'

    def draw(self):
        plt.figure(figsize=(32, 24))
        nx.draw_networkx(self.graph, node_color=['blue' if gene else 'white' for gene in self.genes], with_labels=True)
        plt.show()

    def solve(self) -> 'Solution':
        edges = list(self.graph.edges)

        for i in range(GRAPH_SIZE):
            if self.genes[i]:
                for j in range(len(edges) - 1, -1, -1):
                    if i in edges[j]:
                        edges.pop(j)

        if len(edges) == 0:
            return self

        edges_to_cover: list = random.sample(sorted(edges), len(edges))

        while len(edges_to_cover):
            a, b = edges_to_cover[0]
            self.genes[a] = True
            for j in range(len(edges_to_cover) - 1, -1, -1):
                if a in edges_to_cover[j]:
                    edges_to_cover.pop(j)

        return self

    def local_improvement(self):
        edges = list(self.graph.edges)
        covered_edges = set()
        for i in random.sample(range(GRAPH_SIZE), GRAPH_SIZE):
            if not self.genes[i]:
                continue
            not_covering = True
            for edge in edges:
                if i in edge and edge not in covered_edges:
                    covered_edges.add(edge)
                    not_covering = False

            if not_covering:
                self.genes[i] = False

        assert len(edges) == len(covered_edges)

    def mutate(self):
        for i in range(GRAPH_SIZE):
            self.genes[i] = bool(self.genes[i] - (random.randint(0, 1000) < 1000 * MUTATION_PROBABILITY))

        return self.solve()

    @classmethod
    def crossover_prb(cls, first: 'Solution', second: 'Solution'):
        new_genes = [random.choice((first.genes[i], second.genes[i])) for i in range(GRAPH_SIZE)]

        return cls(first.graph, new_genes)


class Population:
    def __init__(self, graph=None):
        self.graph = graph or nx.fast_gnp_random_graph(GRAPH_SIZE, EDGE_PROBABILITY)

        self.population = [Solution(self.graph).solve() for _ in range(POPULATION_SIZE)]

        self.population.sort(key=lambda x: x.cover_len)

    def nex_gen(self):
        parrent1, parrent2 = random.choices(
            self.population, [1 / solution.cover_len for solution in self.population], k=2
        )
        children: list[Solution] = [Solution.crossover_prb(parrent1, parrent2) for _ in range(POPULATION_SIZE // 2)]

        for child in children:
            child.mutate()
            child.local_improvement()

        self.population = children + self.population

        self.population.sort(key=lambda x: x.cover_len)

        self.population = self.population[:POPULATION_SIZE]

    @property
    def best(self):
        return self.population[0]

    def draw(self):
        plt.figure(figsize=(32, 24))
        nx.draw_networkx(self.graph, with_labels=True)
        plt.show()


ITERATION_COUNT = 1000


def _main():
    pop = Population()
    pop.draw()
    y = []
    for _ in range(ITERATION_COUNT):
        y.append(pop.best.cover_len)
        pop.nex_gen()
    x = np.array(range(ITERATION_COUNT))
    plt.plot(x, y)
    plt.show()
    print(y[0] - y[-1])
    pop.best.draw()


if __name__ == '__main__':
    _main()
