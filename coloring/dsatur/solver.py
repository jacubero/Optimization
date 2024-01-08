#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List, Tuple

class Color:

    index: int
    n_nodes: int

    def __init__(self, index) -> None:
        self.index = index
        self.n_nodes = 0

    def __repr__(self):
        return f"C{self.index}"

    def add_node(self):
        self.n_nodes = self.n_nodes + 1

class Node:

    neighbors: List['Node']
    index: int
    color: Color

    def __init__(self, index):
        self.index = index
        self.neighbors = []
        self.color = None

    def __repr__(self) -> str:
        return f"N{self.index}|{self.color}"

    def add_neighbor(self, node: 'Node'):
        if node not in self.neighbors:
            self.neighbors.append(node)

    def set_color(self, color: Color):
        self.color = color
        color.add_node()

    @property
    def neighbor_colors(self):
        return [n.color for n in self.neighbors if n.color is not None]

    @property
    def saturation(self):
        return len(set((n.color for n in self.neighbors if n.color is not None)))

    @property
    def degree(self):
        return len(self.neighbors)

class DSatur:

    N: List[Node]
    C: List[Color]
    history: List[Node]

    def __init__(self, nodes: List[int], edges: List[Tuple[int, int]]):
        """Graph Coloring DSatur Algorithm proposed by Brélaz (1979)

        Brélaz, D., 1979. New methods to color the vertices of a graph.
        Communications of the ACM, 22(4), 251-256.

        Parameters
        ----------
        nodes : List[int]
            List of node indexes for which colors should be defined

        edges : List[Tuple[int, int]]
            List of edges for which nodes can't be assigned to the same color
        """
        N = [Node(i) for i in nodes]
        for e in edges:
            i, j = e
            N[i].add_neighbor(N[j])
            N[j].add_neighbor(N[i])
        self.N = N
        self.C = []
        self.history = []

    def find_next_color(self, node: Node) -> Color:
        """Finds the next available color to assign to a given node

        Parameters
        ----------
        node : Node
            Node considered in step

        Returns
        -------
        Color
            Next color available
        """
        next_color = None
        for c in self.C:
            if c not in node.neighbor_colors:
                next_color = c
                break
        if next_color is None:
            next_color = Color(len(self.C) + 1)
            self.C.append(next_color)
        return next_color

    def solve(self, save_history=False):
        """Solve the instance

        Parameters
        ----------
        save_history : bool, optional
            Either or not to store a sequence of colores nodes in the `history` attribute,
            by default False
        """
        Q = [n for n in self.N]  # Pool of uncolored nodes
        while len(Q) > 0:
            Q.sort(key=lambda x: (x.saturation, x.degree), reverse=True)
            n: Node = Q.pop(0)
            next_color = self.find_next_color(n)
            n.set_color(next_color)
            if save_history:
                self.history.append(n)
        self.C.sort(key=lambda x: x.n_nodes, reverse=True)

    @property
    def cost(self):
        return len(self.C)

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    node_set = set()
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
        node_set.add(int(parts[0]))
        node_set.add(int(parts[1]))

    nodes = sorted(node_set)
    assert len(nodes) == node_count, "Wrong number of nodes specified"

    dsatur = DSatur(nodes, edges)
    dsatur.solve(save_history=True)

    solution = []
    for node in dsatur.N:
        solution.append(int(str(node).split("|")[1][1:])-1)

    solution_node_set = set(solution)
    num_colors = len(solution_node_set)

    # prepare the solution in the specified output format
    output_data = str(num_colors) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

