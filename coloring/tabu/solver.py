#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import time
from random import randrange, choice, sample
from queue import Queue
from collections import deque

# A dictionary of the list of nodes adjacent to each node
adjacent_dict = {}

# Tabu table
class Tabu:
    def __init__(self, tabu_size):
        self.tabu_hash = set()
        self.tabu_queue = deque()
        self.tabu_size = tabu_size

    def is_find(self, node):
        return node in self.tabu_hash

    def push(self, node):
        if self.is_find(node):
            return

        self.tabu_hash.add(node)
        self.tabu_queue.append(node)

        if len(self.tabu_hash) > self.tabu_size:
            self.pop()

    def pop(self):
        top = self.tabu_queue.popleft()
        self.tabu_hash.remove(top)

# The length of tabu list is set to 1/tabu_ratio_size of the number of nodes
tabu_ratio_size = 10
# Times to retry if we did not find a feasible solution in a given number of steps.
retry_limit = 100
# Maximum step to try. 
# one step means change the color of a node
step_limit = 50000

# Reinitialize color choice for every node
def initialize_color(total_color_count):

    new_color_list = sample(range(total_color_count), total_color_count)
    return new_color_list

# Change the color of a node
def change_color(node, node_neighbor_list, color_list, total_color_count, violation_dict, total_violation):

    # Count the color distribution of neighbor nodes
    color_count = [0] * total_color_count
    for neighbor in node_neighbor_list:
        neighbor_color = color_list[neighbor]
        color_count[neighbor_color] += 1

    min_color_count = float('inf')
    min_color_list = []

    # Select color with least violation with neighbor
    for color in range(total_color_count):
        # skip its own color
        if color == color_list[node]:
            continue

        # If the color violation is smaller than the min color violation, clear the candidate list and add the color to it
        if min_color_count > color_count[color]:
            min_color_count = color_count[color]
            min_color_list = [color]
        
        # If the color violation is the min color violation, add the color to candidate list
        elif min_color_count == color_count[color]:
            min_color_list.append(color)

    # We must find at least one color
    assert min_color_list

    # Random sample a color from the candidate list
    new_color = choice(min_color_list)

    # Update violation for the node and its neighbor
    # Update total violation
    for neighbor in node_neighbor_list:
        if color_list[neighbor] == color_list[node]:
            violation_dict[neighbor] -=1
            violation_dict[node] -=1
            total_violation -= 2
        elif color_list[neighbor] == new_color:
            violation_dict[neighbor] +=1
            violation_dict[node] +=1
            total_violation += 2

    color_list[node] = new_color

# Remove a color from current color choice
# it works like this, suppose there are total 10 colors from 0 ~ 9, the current color choice is:
# 7 1 4 2 5 9 0 3 6 8 5 9 0 4 
# If we want to remove color 5, for each color that is bigger than 5, we minus it by 1:
# 6 1 4 2 5 8 0 3 5 7 5 8 0 4
# then for each color equals to 5 we set it to a random color from 0 ~ 8:
# 6 1 4 2 3 8 0 3 1 7 4 8 0 4

def remove_color(color_list, total_color_count):

    color_to_remove = randrange(total_color_count)
    new_color_list = []

    for c in color_list:
        if c == color_to_remove:
            # For each color equal to color_to_remove, set it to a random color from 0 to total_color_count - 2
            new_color_list.append(randrange(total_color_count - 1))
        elif c > color_to_remove:
            # Decrement the index for colors greater than color_to_remove
            new_color_list.append(c - 1)
        else:
            # Keep the colors less than color_to_remove unchanged
            new_color_list.append(c)

    return new_color_list

# Count violation for every node and count total violation
def init_violation(adjacent_dict, color_list):

    violation_dict = {}
    total_violation = 0

    for node in adjacent_dict:
        violation = 0

        for neighbor in adjacent_dict[node]:
            if color_list[node] == color_list[neighbor]:
                violation += 1

        violation_dict[node] = violation
        total_violation += violation

    return violation_dict, total_violation

# Select next node to change color
def select_next_node(violation_dict, tabu):
    max_violation = float('-inf')
    max_violation_node_list = []

    for node in violation_dict:
        # Skip nodes with no violation
        if violation_dict[node] == 0:
            continue

        # Skip nodes in tabu list
        if tabu.is_find(node):
            continue

        # If violation is max violation, add the node to candidate list
        if max_violation == violation_dict[node]:
            max_violation_node_list.append(node)

        # If violation is bigger than max violation, clear the candidate list and add the node
        elif max_violation < violation_dict[node]:
            max_violation = violation_dict[node]
            max_violation_node_list = [node]

    # If no nodes with violations are available, select a random node from those in the tabu list
    if not max_violation_node_list:
        max_violation_node_list = [node for node in tabu.tabu_hash]

    if not max_violation_node_list:
        return -1

    # Random sample a node from candidate list
    return choice(max_violation_node_list)

# Check feasibility of current number of colors
def is_feasible(adjacent_dict, color_list, total_color_count, tabu_size):

    # one step means change the color of a node
    step_count = 0

    violation_dict, total_violation = init_violation(adjacent_dict, color_list)

    # Tabu hash table and tabu queue, they contain same data
    # use hash table to accelerate retrieval, use queue to make the tabu list FIFO (First In First Out)
    tabu = Tabu(tabu_size)

    while step_count < step_limit and total_violation > 0:

        # Select next node to change color
        node = select_next_node(violation_dict, tabu)

        # If cannot select next node, maybe the tabu list is too long, then pop one element from the tabu list
        while node == -1:
            tabu.pop()
            node = select_next_node(violation_dict, tabu)
        
        # Add the selected node to tabu list
        tabu.push(node)

        # Change color of the selected code
        change_color(node, adjacent_dict[node], color_list, total_color_count, violation_dict, total_violation)
        
        step_count +=1

    return total_violation == 0, step_count

def save_solution(filename, feasible_color_count, feasible_color_list):
    # Write the output to filename
    with open(filename, "w") as f:
        output_data = str(feasible_color_count) + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, feasible_color_list))
        output_data += '\n'
        f.write(output_data)
        f.close()

# Search the minimum number of colors for a graph
# Return the color choice of every node and the total number of colors
def search(adjacent_dict, color_list, init_color_count,node_count):

    # Set the length of tabu list to 1/tabu_ratio_size of the number of nodes
    tabu_limit = max(int(node_count / tabu_ratio_size), 1)

    feasible_color_list = [-1]
    feasible_color_count = -1

    for color_count in range(init_color_count, 1, -1):
        # Times to retry if did not find feasible solution in a given number of steps.
        retry_count = 0

        while True:
            feasible, step_count = is_feasible(adjacent_dict, color_list, color_count, tabu_limit)

            if feasible:
                #print(f"{color_count} colors is feasible, tried {step_count} step")
                feasible_color_list = color_list
                feasible_color_count = color_count
                filename = str(color_count) + ".txt"

                save_solution(filename, feasible_color_count, feasible_color_list)

                color_list = remove_color(feasible_color_list, feasible_color_count)
                break

            retry_count +=1
            if retry_count >= retry_limit:
                 return feasible_color_list, feasible_color_count

            #print(f"[Number of colors {color_count:4d}][Retry {retry_count:5d}] reinitializing color")
            color_list = remove_color(feasible_color_list, feasible_color_count)

    return feasible_color_list, feasible_color_count

def solve_it(input_data,color_data = ""):
    # parse the input data
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        vs = int(parts[0])
        ve = int(parts[1])
        if vs in adjacent_dict:
            adjacent_dict[vs].append(ve)
        else:
            adjacent_dict[vs] = [ve]
        if ve in adjacent_dict:        
            adjacent_dict[ve].append(vs)
        else:
            adjacent_dict[ve] = [vs]

    if color_data == "":
        color_list = initialize_color(node_count)
        init_color_count = node_count
    else:
        # parse the color data if exists file with initial results
        lines = color_data.split('\n')

        first_line = lines[0].split()
        init_color_count = int(first_line[0])
        color_list = list(map(int, lines[1].split()))

    feasible_color_list, feasible_color_count = search(adjacent_dict, color_list, init_color_count, node_count)

    # Prepare the solution in the specified output format
    output_data = str(feasible_color_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, feasible_color_list))

    return output_data

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

