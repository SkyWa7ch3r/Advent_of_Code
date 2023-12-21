import numpy as np
import networkx as nx
import cugraph as cnx
import time

def solution():
    input = np.array([list(line) for line in np.loadtxt('test3.txt', dtype = str)])
    start = np.where(input == 'S')
    start = (start[0].item(), start[1].item())
    # Directed graph, we're going to assume pipes have a one-way flow for simplicity
    # Nodes are pipe pieces, and edges represent the flow of the pipes
    pipes = nx.DiGraph()
    pipes.add_node(start)
    stack = [start]
    seen_nodes = set()
    max_row, max_col = input.shape
    left_checker = ['.', '|', '7', 'J', 'S']
    above_checker = ['.', '-', 'L', 'J', 'S']
    right_checker = ['.', '|', 'F', 'L', 'S']
    below_checker = ['.', '-', 'F', '7', 'S']
    print("Start", start)
    # The goal here is going to be finding the loops, and get the longest loop
    # from the start and do length + 1 / 2 which should get us our desired answer
    # This pretty much means create directed graph, get longest path back to the start, 
    # divide that path length by 2
    while len(stack) > 0:
        node = stack.pop()
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
                    stack.append((node[0] - 1, node[1]))
                if node[1] - 1 >= 0 and input[node[0], node[1] - 1] not in left_checker:
                    pipes.add_node((node(0), node[1] - 1))
                    pipes.add_edge((node(0), node[1] - 1), node)
                    stack.append((node(0), node[1] - 1))
                if node[1] + 1 < max_col and input[node[0], node[1] + 1] not in right_checker:
                    pipes.add_node((node[0], node[1] + 1))
                    pipes.add_edge(node, (node[0], node[1] + 1))
                    stack.append((node[0], node[1] + 1))
                if node[0] + 1 < max_row and input[node[0] + 1, node[1]] not in below_checker:
                    pipes.add_node((node[0] + 1, node[1]))
                    pipes.add_edge(node, (node[0] + 1, node[1]))
                    stack.append((node[0] + 1, node[1]))
            case '|':
                # Check above and below
                if node[0] - 1 >= 0 and\
                    input[node[0] - 1, node[1]] not in above_checker and\
                    (node[0] - 1, node[1]) not in pipes.neighbors(node):
                    pipes.add_node((node[0] - 1, node[1]))
                    pipes.add_edge((node[0] - 1, node[1]), node)
                    stack.append((node[0] - 1, node[1]))
                if node[0] + 1 < max_row and\
                    input[node[0] + 1, node[1]] not in below_checker and\
                    (node[0] + 1, node[1]) not in pipes.neighbors(node):
                    pipes.add_node((node[0] + 1, node[1]))
                    pipes.add_edge(node, (node[0] + 1, node[1]))
                    stack.append((node[0] + 1, node[1]))
            case '-':
                # Check Left and Right
                if node[1] - 1 >= 0 and \
                    input[node[0], node[1] - 1] not in left_checker and\
                    (node[0], node[1] - 1) not in pipes.neighbors(node):
                    pipes.add_node((node[0], node[1] - 1))
                    pipes.add_edge((node[0], node[1] - 1), node)
                    stack.append((node[0], node[1] - 1))
                if node[1] + 1 < max_col and \
                    input[node[0], node[1] + 1] not in right_checker and\
                    (node[0], node[1] + 1) not in pipes.neighbors(node):
                    pipes.add_node((node[0], node[1] + 1))
                    pipes.add_edge(node, (node[0], node[1] + 1))
                    stack.append((node[0], node[1] + 1))
            case 'L':
                # Check Above and Right
                if node[0] - 1 >= 0 and\
                    input[node[0] - 1, node[1]] not in above_checker and\
                    (node[0] - 1, node[1]) not in pipes.neighbors(node):
                    pipes.add_node((node[0] - 1, node[1]))
                    pipes.add_edge((node[0] - 1, node[1]), node)
                    stack.append((node[0] - 1, node[1]))
                if node[1] + 1 < max_col and \
                    input[node[0], node[1] + 1] not in right_checker and\
                    (node[0], node[1] + 1) not in pipes.neighbors(node):
                    pipes.add_node((node[0], node[1] + 1))
                    pipes.add_edge(node, (node[0], node[1] + 1))
                    stack.append((node[0], node[1] + 1))
            case 'J':
                # Check Above and Left
                if node[0] - 1 >= 0 and\
                    input[node[0] - 1, node[1]] not in above_checker and\
                    (node[0] - 1, node[1]) not in pipes.neighbors(node):
                    pipes.add_node((node[0] - 1, node[1]))
                    pipes.add_edge((node[0] - 1, node[1]), node)
                    stack.append((node[0] - 1, node[1]))
                if node[1] - 1 >= 0 and \
                    input[node[0], node[1] - 1] not in left_checker and\
                    (node[0], node[1] - 1) not in pipes.neighbors(node):
                    pipes.add_node((node[0], node[1] - 1))
                    pipes.add_edge((node[0], node[1] - 1), node)
                    stack.append((node[0], node[1] - 1))
            case '7':
                # Check Left and Below
                if node[1] - 1 >= 0 and \
                    input[node[0], node[1] - 1] not in left_checker and\
                    (node[0], node[1] - 1) not in pipes.neighbors(node):
                    pipes.add_node((node[0], node[1] - 1))
                    pipes.add_edge((node[0], node[1] - 1), node)
                    stack.append((node[0], node[1] - 1))
                if node[0] + 1 < max_row and\
                    input[node[0] + 1, node[1]] not in below_checker and\
                    (node[0] + 1, node[1]) not in pipes.neighbors(node):
                    pipes.add_node((node[0] + 1, node[1]))
                    pipes.add_edge(node, (node[0] + 1, node[1]))
                    stack.append((node[0] + 1, node[1]))
            case 'F':
                # Check Below and Right
                if node[0] + 1 < max_row and\
                    input[node[0] + 1, node[1]] not in below_checker and\
                    (node[0] + 1, node[1]) not in pipes.neighbors(node):
                    pipes.add_node((node[0] + 1, node[1]))
                    pipes.add_edge(node, (node[0] + 1, node[1]))
                    stack.append((node[0] + 1, node[1]))
                if node[1] + 1 < max_col and \
                    input[node[0], node[1] + 1] not in right_checker and\
                    (node[0], node[1] + 1) not in pipes.neighbors(node):
                    pipes.add_node((node[0], node[1] + 1))
                    pipes.add_edge(node, (node[0], node[1] + 1))
                    stack.append((node[0], node[1] + 1))
            case _:
                continue
        print(stack)
    print(pipes.nodes)
    print(pipes.edges)
    print(pipes)

start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")