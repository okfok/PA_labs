import random

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

GRAPH_SIZE = 300
EDGE_PROBABILITY = 0.05

POPULATION_SIZE = 10
CROSSOVER_COUNT = 1
MUTATION_PROBABILITY = 0.005
MUTATION_MAX_COUNT = 10


class Solution:
    def __init__(self, graph=None, genes=None):
        self.graph = graph or nx.gnp_random_graph(GRAPH_SIZE, EDGE_PROBABILITY)
        self.genes = genes or [False for _ in range(GRAPH_SIZE)]

    @property
    def cover_len(self) -> int:
        return sum(self.genes)

    def __repr__(self) -> str:
        return f'Sol({self.cover_len})'

    def draw(self) -> None:
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

    @property
    def is_solved(self) -> bool:
        edges = list(self.graph.edges)

        for i in range(GRAPH_SIZE):
            if self.genes[i]:
                for j in range(len(edges) - 1, -1, -1):
                    if i in edges[j]:
                        edges.pop(j)

        return len(edges) == 0

    def local_improvement(self) -> 'Solution':
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

        assert self.is_solved
        return self

    def mutate_prb(self) -> 'Solution':
        for i in range(GRAPH_SIZE):
            self.genes[i] = bool(self.genes[i] - (random.randint(0, 1000) < 1000 * MUTATION_PROBABILITY))

        return self

    def mutate_max(self) -> 'Solution':
        indexes_to_mutate = random.sample(range(GRAPH_SIZE), random.randint(1, MUTATION_MAX_COUNT))
        for i in indexes_to_mutate:
            self.genes[i] = bool(self.genes[i] - True)

        return self

    @classmethod
    def crossover_prb(cls, first: 'Solution', second: 'Solution') -> list['Solution']:
        new_genes = [random.choice((first.genes[i], second.genes[i])) for i in range(GRAPH_SIZE)]

        return [cls(first.graph, new_genes)]

    @classmethod
    def crossover_one_point(cls, first: 'Solution', second: 'Solution') -> list['Solution']:
        point = random.randint(1, GRAPH_SIZE - 1)

        return [
            cls(first.graph, first.genes[:point] + second.genes[point:]),
            cls(first.graph, second.genes[:point] + first.genes[point:])
        ]

    @classmethod
    def crossover_two_point(cls, first: 'Solution', second: 'Solution') -> list['Solution']:
        point1 = random.randint(1, GRAPH_SIZE // 2)
        point2 = random.randint(GRAPH_SIZE // 2 + 1, GRAPH_SIZE - 1)

        return [
            cls(first.graph, first.genes[:point1] + second.genes[point1:point2] + first.genes[point2:]),
            cls(first.graph, second.genes[:point1] + first.genes[point1:point2] + second.genes[point2:])
        ]

    def copy(self):
        return self.__class__(self.graph, self.genes.copy())


class Population:
    def __init__(self, graph=None):
        self.graph = graph or nx.fast_gnp_random_graph(GRAPH_SIZE, EDGE_PROBABILITY)

        self.population = [Solution(self.graph).solve() for _ in range(POPULATION_SIZE)]

        self.population.sort(key=lambda x: x.cover_len)

    def nex_gen(self):
        parrent1, parrent2 = random.choices(
            self.population, [1 / solution.cover_len for solution in self.population], k=2
        )
        children: list[Solution] = [
            child for child in
            Solution.crossover_two_point(parrent1, parrent2) for _ in range(CROSSOVER_COUNT)  # crossover
            if child.is_solved
        ]

        if len(children):
            self.population += [child.copy() for child in children]

            mutated_children = list(
                filter(lambda x: x.is_solved, [child.mutate_max() for child in children]))  # mutation
            if len(mutated_children):
                self.population += [child.copy() for child in mutated_children]

                improved_children = list(
                    filter(lambda x: x.is_solved,
                           [child.local_improvement() for child in mutated_children]))  # improvement
                if len(improved_children):
                    self.population += improved_children

        self.population = random.sample(self.population, len(self.population))

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
    # pop.draw()
    y = []
    for _ in range(ITERATION_COUNT):
        y.append(pop.best.cover_len)
        pop.nex_gen()
    x = np.array(range(ITERATION_COUNT))
    plt.plot(x, y)
    plt.show()
    print(y[0] - y[-1])
    # pop.best.draw()
    return y[0] - y[-1]


def _test():
    print(sum([_main() for _ in range(5)]) / 5)


if __name__ == '__main__':
    _main()
