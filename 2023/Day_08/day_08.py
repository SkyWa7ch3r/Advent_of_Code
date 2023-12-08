import cupy as cp
import cudf as cd
import cugraph as cg
import networkx as nx
import time

def solution():
    input = cd.read_text('test1.txt', delimiter = '\n', strip_delimiters = True)
    instructions = input.iloc[0]
    input = input[2:].str.partition('=').loc[:, [0,2]]
    nodes = input[0]
    edges = input[2].str.strip()
    print(instructions, '\n', nodes, '\n', edges)

    network = nx.DiGraph()
    network.add_nodes_from(nodes.to_arrow().to_pylist())
    print(network)


start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")