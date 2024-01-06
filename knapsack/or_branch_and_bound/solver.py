#!/usr/bin/python
# -*- coding: utf-8 -*-

from ortools.algorithms.python import knapsack_solver

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    capacities = []
    capacities.append(capacity)

    values = []
    weights = [[]]

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        values.append(int(parts[0]))
        weights[0].append(int(parts[1]))

    # Create the solver.
    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        "KnapsackExample",
    )

    solver.init(values, weights, capacities)
    value = solver.solve()

    taken = [0]*item_count

    for index in range(item_count):
        if solver.best_solution_contains(index):
            taken[index] = 1
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

