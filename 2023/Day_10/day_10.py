import numpy as np
import networkx as nx
import cugraph as cnx
import time

def solution():
    input = np.array([list(line) for line in np.loadtxt('test1.txt', dtype = str)])
    start = np.where(input == 'S')
    start = (start[0].item(), start[1].item())
    # Directed graph, we're going to assume pipes have a one-way flow for simplicity
    # Nodes are pipe pieces, and edges represent the flow of the pipes
    pipes = nx.DiGraph()
    pipes.add_node(start)
    stack = [start]
    max_row, max_col = input.shape
    left_checker = ['.', '|', '7', 'J']
    above_checker = ['.', '-', 'L', 'J']
    right_checker = ['.', '|', 'F', 'L']
    below_checker = ['.', '-', 'F', '7']
    # The goal here is going to be finding the loops, and get the longest loop
    # from the start and do length + 1 / 2 which should get us our desired answer
    # This pretty much means create directed graph, get longest path back to the start, 
    # divide that path length by 2
    while len(stack ) > 0:
        node = stack.pop()
        # Check Left
        if node[1] - 1 >= 0 and input[node[0], node[1] - 1] not in left_checker:
            left = input[node[0], node[1] - 1]
            pipes.add_node((node(0), node[1] - 1))
            pipes.add_edge([(node(0), node[1] - 1), node])
            stack.append((node(0), node[1] - 1))
            if left == 'F' and node[0] + 1 < max_row and input[node[0] + 1, node[1] - 1] not in below_checker:
                pipes.add_node((node[0] + 1, node[1] - 1))
                pipes.add_edge([(node[0] + 1, node[1] - 1), (node(0), node[1] - 1)])
                stack.append((node[0] + 1, node[1] - 1))
            elif left == 'L' and node[0] - 1 >= 0 and input[node[0] - 1, node[1] - 1] not in above_checker:
                pipes.add_node((node[0] - 1, node[1] - 1))
                pipes.add_edge([(node[0] - 1, node[1] - 1), (node(0), node[1] - 1)])
                stack.append((node[0] - 1, node[1] - 1))
        # Check Above
        if node[0] - 1 >= 0 and input[node[0] - 1, node[1]] not in above_checker:
            above = input[node[0] - 1, node[1]]
            pipes.add_node((node[0] - 1, node[1]))
            pipes.add_edge([(node[0] - 1, node[1]), node])
            stack.append((node[0] - 1, node[1]))
            if above == 'F' and node[1] + 1 < max_col and input[node[0] - 1, node[1] + 1] not in right_checker:
                pipes.add_node((node[0] - 1, node[1] + 1))
                pipes.add_edge([(node[0] - 1, node[1]), (node(0) - 1, node[1] + 1)])
                stack.append((node(0) - 1, node[1] + 1))
            if above == '7' and node[1] - 1 >= 0 and input[node[0] - 1, node[1] - 1] not in left_checker:
                pipes.add_node((node[0] - 1, node[1] - 1))
                pipes.add_edge([(node[0] - 1, node[1]), (node(0) - 1, node[1] - 1)])
                stack.append((node(0) - 1, node[1] - 1))
        # Check Right
        if node[1] + 1 < max_col and input[node[0], node[1] + 1] not in right_checker:
            right = input[node[0], node[1] + 1]
            pipes.add_node((node[0], node[1] + 1))
            pipes.add_edge([node, (node[0], node[1] + 1)])
            stack.append((node[0], node[1] + 1))
            if right == 'J' and node[0] - 1 >= 0 and input[node[0] - 1, node[1] + 1] not in above_checker:
                pipes.add_node((node[0] - 1, node[1] + 1))
                pipes.add_edge([(node[0] - 1, node[1] + 1), (node[0], node[1] + 1)])
                stack.append((node[0] - 1, node[1] + 1))
            if right == '7' and node[0] + 1 < max_row and input[node[0] + 1, node[1] + 1] not in below_checker:
                pipes.add_node((node[0] + 1, node[1] + 1))
                pipes.add_edge([(node[0], node[1] + 1), ])
        # Check Below
        if node[0] + 1 < max_row and input[node[0] + 1, node[1]] not in below_checker:
            pass
    print(pipes)


start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")