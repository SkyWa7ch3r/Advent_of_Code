import networkx as nx
import numpy as np
from scipy.ndimage import maximum_filter

def lowest_risk(file, multiply = 1):
    inputs = np.char.strip(np.array(open(file, 'r').readlines()))
    risk_levels = np.zeros((inputs.shape[0], len(inputs[0])), dtype = np.int64)
    for i in range(inputs.shape[0]):
        line = np.array(list(inputs[i]))
        risk_levels[i, :] = line
    rows, cols = risk_levels.shape
    # TIle it out
    risk_levels = np.tile(risk_levels, (multiply, multiply))
    shaper = risk_levels.shape[1] // multiply
    # Create a tile structure [[0, 1],[1,2]] ...
    adder = np.tile(np.tile(np.repeat(np.arange(multiply), shaper), shaper).reshape((shaper, risk_levels.shape[1])), (multiply, 1))
    # Create another tile structure [[0,0],[1,1]]...
    incrementer = np.repeat(np.repeat(np.arange(multiply),risk_levels.shape[1]).reshape(multiply, risk_levels.shape[1]), shaper, axis = 0)
    # Add them together
    adder = adder + incrementer
    # Add to risk levels
    risk_levels = risk_levels + adder
    # Now that we've added it
    risk_levels[np.where(risk_levels > 9)] = risk_levels[np.where(risk_levels > 9)] % 9
    nodes = np.arange(risk_levels.size)
    risk_levels_iter = risk_levels.flat
    risk_network = nx.MultiDiGraph()
    for node in nodes:
            if node % 1000 == 0:
                print(node)
            zeros = np.zeros_like(risk_levels)
            zeros.flat[node] = 1
            edges = maximum_filter(zeros, footprint = [[0,1,0],[1,0,1],[0,1,0]])
            edges.flat[node] = 0
            edges = np.nonzero(edges.flat)[0]
            for edge in edges:
                risk_network.add_edge(node, edge, weight = risk_levels_iter[edge])
    return nx.shortest_path_length(risk_network, source = nodes[0], target = nodes[-1], weight='weight')



if __name__ == '__main__':
    # Part 1
    print(lowest_risk('test.txt'))
    assert lowest_risk('test.txt') == 40
    print(lowest_risk('input.txt'))
    # Part 2
    print(lowest_risk('test.txt', multiply = 5))
    assert lowest_risk('test.txt', multiply = 5) == 315
    print(lowest_risk('input.txt', multiply = 5))
