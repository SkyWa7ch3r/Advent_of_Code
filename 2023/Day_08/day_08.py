import cudf as cd
import itertools
import time
import numpy as np
from numba import cuda

@cuda.jit
def get_all_z(node_list, end_list, left, right, instructions, steps):
    node_idx = cuda.grid(1)
    if node_idx < node_list.size:
        found = False
        instruction = 0
        current = node_list[node_idx]
        while not found:
            if instructions[instruction] == 0:
                current = left[current]
            else:
                current = right[current]
            steps[node_idx] += 1
            instruction += 1
            if instruction == instructions.size:
                instruction = 0
            for num in end_list:
                if num == current:
                    found = True


def solution():
    input = cd.read_text('input.txt', delimiter = '\n', strip_delimiters = True)
    instructions = input.iloc[0].strip()
    input = input[2:].str.partition('=').loc[:, [0,2]]
    nodes = input[0].str.strip().to_arrow().to_pylist()
    edges = input[2].str.strip().str.replace("\(|\)|\s", '').str.split(',')
    edges = edges.to_arrow().to_pylist()
    network = {}
    current = 'AAA'
    end = 'ZZZ'
    network = {node: {'L' : edge[0], 'R': edge[1]} for node, edge in zip(nodes, edges)}
    # Solution for Part 1
    if 'AAA' in list(network.keys()):
        steps = 0
        for instruction in itertools.cycle(instructions):
            current = network[current][instruction]
            steps += 1
            if current == end:
                break
        print(f"The number of steps to ZZZ was: {steps}")
    # Part 2 Solutions
    # Convert all to numbers for parallel compute using GPU
    node_dict = {node: idx for idx, node in enumerate(nodes)}
    left = []
    right = []
    for edge in edges:
        left.append(node_dict[edge[0]])
        right.append(node_dict[edge[1]])
    left = np.array(left)
    right = np.array(right)
    numbered_instructions = np.array(list(instructions.replace('L', '0').replace('R', '1')), dtype = np.int64)
    node_list = np.array([node_dict[a_node] for a_node in filter(lambda x: x[-1] == 'A' ,list(network.keys()))])
    end_list = np.array([node_dict[z_node] for z_node in filter(lambda x: x[-1] == 'Z' ,list(network.keys()))])
    steps = np.zeros_like(node_list)
    threads = 1024
    blocks = (node_list.size + threads - 1) // threads
    get_all_z[blocks, threads](node_list, end_list, left, right, numbered_instructions, steps)
    print(f"The number of steps required to get all z {np.lcm.reduce(steps)}")


start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")