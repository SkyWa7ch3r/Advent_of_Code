import numpy as np
import networkx as nx
import cugraph as cnx
from collections import deque
from scipy.ndimage import label
import time

def solution():
    input = np.array([list(line) for line in np.loadtxt('input.txt', dtype = str)])
    start = np.where(input == 'S')
    start = (start[0].item(), start[1].item())
    # Directed graph, we're going to assume pipes have a one-way flow for simplicity
    # Nodes are pipe pieces, and edges represent the flow of the pipes
    pipes = nx.Graph()
    pipes.add_node(start)
    queue = deque([start])
    seen_nodes = set()
    max_row, max_col = input.shape
    left_checker = ['.', '|', '7', 'J', 'S']
    above_checker = ['.', '-', 'L', 'J', 'S']
    right_checker = ['.', '|', 'F', 'L', 'S']
    below_checker = ['.', '-', 'F', '7', 'S']
    # The goal here is going to be finding the loops, and get the longest loop
    # from the start and do length + 1 / 2 which should get us our desired answer
    # This pretty much means create directed graph, get longest path back to the start, 
    # divide that path length by 2
    while len(queue) > 0:
        node = queue.popleft()
        if node in seen_nodes:
            continue
        seen_nodes.add(node)
        pipe_type = input[node]
        match pipe_type:
            case 'S':
                # Check above, left, right and below
                if node[0] - 1 >= 0 and input[node[0] - 1, node[1]] not in above_checker:
                    pipes.add_node((node[0] - 1, node[1]))
                    pipes.add_edge((node[0] - 1, node[1]), node)
                    queue.append((node[0] - 1, node[1]))
                if node[1] - 1 >= 0 and input[node[0], node[1] - 1] not in left_checker:
                    pipes.add_node((node[0], node[1] - 1))
                    pipes.add_edge((node[0], node[1] - 1), node)
                    queue.append((node[0], node[1] - 1))
                if node[1] + 1 < max_col and input[node[0], node[1] + 1] not in right_checker:
                    pipes.add_node((node[0], node[1] + 1))
                    pipes.add_edge(node, (node[0], node[1] + 1))
                    queue.append((node[0], node[1] + 1))
                if node[0] + 1 < max_row and input[node[0] + 1, node[1]] not in below_checker:
                    pipes.add_node((node[0] + 1, node[1]))
                    pipes.add_edge(node, (node[0] + 1, node[1]))
                    queue.append((node[0] + 1, node[1]))
            case '|':
                # Check above and below
                if node[0] - 1 >= 0 and\
                    input[node[0] - 1, node[1]] not in above_checker and\
                    (node[0] - 1, node[1]) not in pipes.neighbors(node):
                    pipes.add_node((node[0] - 1, node[1]))
                    pipes.add_edge((node[0] - 1, node[1]), node)
                    queue.append((node[0] - 1, node[1]))
                if node[0] + 1 < max_row and\
                    input[node[0] + 1, node[1]] not in below_checker and\
                    (node[0] + 1, node[1]) not in pipes.neighbors(node):
                    pipes.add_node((node[0] + 1, node[1]))
                    pipes.add_edge(node, (node[0] + 1, node[1]))
                    queue.append((node[0] + 1, node[1]))
            case '-':
                # Check Left and Right
                if node[1] - 1 >= 0 and \
                    input[node[0], node[1] - 1] not in left_checker and\
                    (node[0], node[1] - 1) not in pipes.neighbors(node):
                    pipes.add_node((node[0], node[1] - 1))
                    pipes.add_edge((node[0], node[1] - 1), node)
                    queue.append((node[0], node[1] - 1))
                if node[1] + 1 < max_col and \
                    input[node[0], node[1] + 1] not in right_checker and\
                    (node[0], node[1] + 1) not in pipes.neighbors(node):
                    pipes.add_node((node[0], node[1] + 1))
                    pipes.add_edge(node, (node[0], node[1] + 1))
                    queue.append((node[0], node[1] + 1))
            case 'L':
                # Check Above and Right
                if node[0] - 1 >= 0 and\
                    input[node[0] - 1, node[1]] not in above_checker and\
                    (node[0] - 1, node[1]) not in pipes.neighbors(node):
                    pipes.add_node((node[0] - 1, node[1]))
                    pipes.add_edge((node[0] - 1, node[1]), node)
                    queue.append((node[0] - 1, node[1]))
                if node[1] + 1 < max_col and \
                    input[node[0], node[1] + 1] not in right_checker and\
                    (node[0], node[1] + 1) not in pipes.neighbors(node):
                    pipes.add_node((node[0], node[1] + 1))
                    pipes.add_edge(node, (node[0], node[1] + 1))
                    queue.append((node[0], node[1] + 1))
            case 'J':
                # Check Above and Left
                if node[0] - 1 >= 0 and\
                    input[node[0] - 1, node[1]] not in above_checker and\
                    (node[0] - 1, node[1]) not in pipes.neighbors(node):
                    pipes.add_node((node[0] - 1, node[1]))
                    pipes.add_edge(node, (node[0] - 1, node[1]))
                    queue.append((node[0] - 1, node[1]))
                if node[1] - 1 >= 0 and \
                    input[node[0], node[1] - 1] not in left_checker and\
                    (node[0], node[1] - 1) not in pipes.neighbors(node):
                    pipes.add_node((node[0], node[1] - 1))
                    pipes.add_edge((node[0], node[1] - 1), node)
                    queue.append((node[0], node[1] - 1))
            case '7':
                # Check Left and Below
                if node[1] - 1 >= 0 and \
                    input[node[0], node[1] - 1] not in left_checker and\
                    (node[0], node[1] - 1) not in pipes.neighbors(node):
                    pipes.add_node((node[0], node[1] - 1))
                    pipes.add_edge((node[0], node[1] - 1), node)
                    queue.append((node[0], node[1] - 1))
                if node[0] + 1 < max_row and\
                    input[node[0] + 1, node[1]] not in below_checker and\
                    (node[0] + 1, node[1]) not in pipes.neighbors(node):
                    pipes.add_node((node[0] + 1, node[1]))
                    pipes.add_edge(node, (node[0] + 1, node[1]))
                    queue.append((node[0] + 1, node[1]))
            case 'F':
                # Check Below and Right
                if node[0] + 1 < max_row and\
                    input[node[0] + 1, node[1]] not in below_checker and\
                    (node[0] + 1, node[1]) not in pipes.neighbors(node):
                    pipes.add_node((node[0] + 1, node[1]))
                    pipes.add_edge((node[0] + 1, node[1]), node)
                    queue.append((node[0] + 1, node[1]))
                if node[1] + 1 < max_col and \
                    input[node[0], node[1] + 1] not in right_checker and\
                    (node[0], node[1] + 1) not in pipes.neighbors(node):
                    pipes.add_node((node[0], node[1] + 1))
                    pipes.add_edge(node, (node[0], node[1] + 1))
                    queue.append((node[0], node[1] + 1))
            case _:
                continue
    nodes = np.concatenate(nx.find_cycle(pipes, start))
    print("The number of steps along the loop to get from the starting position to the farthest point is" , nodes.shape[0] // 4, "steps")
    nodes = ((nodes[:, 0]), (nodes[:, 1]))
    to_label = input.copy()
    to_label[nodes] = 0
    to_label[to_label != '0'] = 1
    to_label = to_label.astype(int)
    labels, _ = label(to_label, structure=np.ones(9).reshape(3,3))
    edges = [labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]]
    edges = np.sort(np.unique(np.concatenate(edges)))
    edges = edges[np.nonzero(edges)]
    labels.flat[np.in1d(labels.flat, edges)] = 0
    rows = np.unique(np.where(labels > 1)[0])
    np.set_printoptions(linewidth=200)
    for row in rows:
        elements = np.nonzero(labels[row, :])[0]
        actual_row = input[row, :]
        north = (actual_row == '|') | (actual_row == 'L') | (actual_row == 'J')
        node_values = to_label[row, :] == 0
        borders = (north & node_values).astype(int)
        for element in elements:
            if np.count_nonzero(borders[:element]) % 2 == 0:
                labels[row, :] = 0
    print(np.count_nonzero(labels))

    
start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")