#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://github.com/bruscalia/optimization-demo-files/blob/1fa7a3825421d0b166195d890f2629c576cfbfda/graph-coloring/graph_coloring.ipynb

from typing import List, Tuple
from random import sample
import pyomo.environ as pyo

# Fill every node with some color
def fill_cstr(model, i):
    return sum(model.x[i, :]) == 1

# Do not repeat colors on edges and color is used
def edge_cstr(model, i, j, c):
    return model.x[i, c] + model.x[j, c] <= model.y[c]

# Break symmetry by setting a preference order
def break_symmetry(model, c):
    if model.C.first() == c:
        return 0 <= model.y[c]
    else:
        c_prev = model.C.prev(c)
        return model.y[c] <= model.y[c_prev]

# Total number of colors used
def obj(model):
    return sum(model.y[:])

def build_ilp(
    nodes: List[int],
    colors: List[int],
    edges: List[Tuple[int, int]]
) -> pyo.ConcreteModel:
    """Instantiates pyomo Integer Linear Programming model for the Graph Coloring Problem

    Parameters
    ----------
    nodes : List[int]
        Node indexes

    colors : List[int]
        List of available colors

    edges : List[Tuple[int, int]]
        Connected edges

    Returns
    -------
    pyo.ConcreteModel
        `Concretemodel` of pyomo
    """

    # Create instance
    model = pyo.ConcreteModel()

    # Create sets
    model.C = pyo.Set(initialize=colors)  # Colors
    model.N = pyo.Set(initialize=nodes)  # Nodes
    model.E = pyo.Set(initialize=edges)  # Edges

    # Create variables
    model.x = pyo.Var(model.N, model.C, within=pyo.Binary)
    model.y = pyo.Var(model.C, within=pyo.Binary)

    # Create constraints
    model.fill_cstr = pyo.Constraint(model.N, rule=fill_cstr)
    model.edge_cstr = pyo.Constraint(model.E, model.C, rule=edge_cstr)
    model.break_symmetry = pyo.Constraint(model.C, rule=break_symmetry)

    # Create objective
    model.obj = pyo.Objective(rule=obj)

    return model

def warmstart_from_data(model, nodes, colors):

    color_set=set(colors)

    for n in nodes:
        for c in color_set:
            if c is colors[n]:
                model.x[n, c].value = 1.0
            else:
                model.x[n, c].value = 0.0

    for c in color_set:
        model.y[c].value = 1.0

def ilp_from_data(nodes, colors, edges) -> pyo.ConcreteModel:
    """Instantiates pyomo Integer Linear Programming model for the Graph Coloring Problem

    Parameters
    ----------
    nodes : List of nodes
    colors : List of colors
    edges : List of edges

    Returns
    -------
    pyo.ConcreteModel
        `Concretemodel` of pyomo
    """
    model = build_ilp(nodes, colors, edges)
    warmstart_from_data(model, nodes, colors)
    return model

# Initialize color choice for every node
def initialize_color(total_color_count):

    new_color_list = sample(range(total_color_count), total_color_count)
    return new_color_list

def solve_it(input_data,color_data = ""):
    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges_list = []
    node_set = set()
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges_list.append((int(parts[0]), int(parts[1])))
        node_set.add(int(parts[0]))
        node_set.add(int(parts[1]))

    nodes_list = sorted(node_set)
    assert len(nodes_list) == node_count, "Wrong number of nodes specified"

    if color_data == "":
        colors_list = initialize_color(node_count)
    else:
        # parse the color data if exists file with initial results
        lines = color_data.split('\n')

        first_line = lines[0].split()
        init_color_count = int(first_line[0])
        colors_list = list(map(int, lines[1].split()))

    ilp = ilp_from_data(nodes_list, colors_list, edges_list)
    opt = pyo.SolverFactory("appsi_highs")
    res = opt.solve(ilp)

    colors = []
    nodes = []
    for n in ilp.N:
        nodes.append(n)
        for c in ilp.C:
            if round(ilp.x[n, c].value, ndigits=0) == 1:
                colors.append(c)

    solution = []
    for col in colors:
        solution.append(col)

    solution_node_set = set(solution)
    num_colors = len(solution_node_set)

    # prepare the solution in the specified output format
    output_data = str(num_colors) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        data_file_location = sys.argv[1].strip()
        with open(data_file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))

    elif len(sys.argv) == 3:
        data_file_location = sys.argv[1].strip()
        with open(data_file_location, 'r') as input_data_file:
            input_data = input_data_file.read()

        color_file_location = sys.argv[2].strip()
        with open(color_file_location, 'r') as color_data_file:
            color_data = color_data_file.read()

        print(solve_it(input_data, color_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

