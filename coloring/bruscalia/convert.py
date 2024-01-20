#!/usr/bin/python
# -*- coding: utf-8 -*-

def convert_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    output_data = 'p edges ' + lines[0] + '\n'
    for i in range(1, edge_count):
        line = lines[i]
        output_data += 'e ' + line + '\n'

    output_data += 'e ' + lines[edge_count]

    return output_data

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(convert_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

