#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def get_expectation(items, capacity, start):

    expectation = 0.0
    for i in range(start, len(items)):
        item = items[i]
        
        if capacity >= item.weight:
            expectation += item.value
            capacity -= item.weight
        
        # If current capacity is not enough to carry the whole item, then put a fraction of it into the knapsack
        # and add the same fraction of its value to the expectation
        else:
            expectation += item.value * capacity / item.weight
            break

    return expectation

def search(items, capacity):
    
    list_size = len(items)
    max_value = 0.0
    max_taken = [0]*list_size

    # To prevent from stack-overflow, instead of using plain recursion here I maintain the stack myself
    # a stack element includes 5 parts:
    # value:         value accumulated so far
    # capacity:      left capacity
    # expectation:   upper bound of value that can get with the left capacity
    # taken:         current take/no-take choice of each item
    # pos:           next item to consider

    start_value = 0.0
    start_capacity = capacity
    start_expectation = get_expectation(items, capacity, 0)
    start_taken = [0]*list_size
    start_pos = 0

    StackElem = namedtuple("StackElem", ['value', 'capacity', 'expectation', 'taken', 'pos'])
    stack = []
    stack.append(StackElem(start_value, start_capacity, start_expectation, start_taken, start_pos))

    while stack:
        Current = stack.pop()

        # If left capacity is not enough, then backtrack
        if Current.capacity < 0:
            continue
        
        # If current expectation is smaller than the best value, then backtrack
        if Current.expectation <= max_value:
            continue

        # If next item to consider does not exist, then backtrack
        if Current.pos >= list_size:
            # If max value is smaller than current value, update max value and its item-take choices
            if max_value < Current.value:
                max_value = Current.value
                max_taken = Current.taken

            continue

        CurrentItem = items[Current.pos]

        # Try not to take the next item
        notake_value = Current.value
        notake_capacity = Current.capacity
        notake_expectation = notake_value + get_expectation(items, notake_capacity, Current.pos + 1)
        notake_taken = Current.taken.copy()

        stack.append(StackElem(notake_value, notake_capacity, notake_expectation, notake_taken, Current.pos + 1))

        # Try to take the next item
        take_value = Current.value + CurrentItem.value
        take_capacity = Current.capacity - CurrentItem.weight
        take_expectation = take_value + get_expectation(items, take_capacity, Current.pos + 1)
        take_taken = Current.taken.copy()
        take_taken[CurrentItem.index] = 1

        stack.append(StackElem(take_value, take_capacity, take_expectation, take_taken, Current.pos + 1))

    return max_value, max_taken

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    sorted_items = sorted(items, key=lambda x: getattr(x, 'value')/getattr(x, 'weight'), reverse=True)
    
    value, taken = search(sorted_items, capacity)
    
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

