import networkx as nx
import queue


def create_network(file):
    cave_system = nx.MultiGraph()
    inputs = open(file, "r").readlines()
    for path in inputs:
        first_cave, second_cave = path.strip().split("-")
        # Swap caves if we have start as second, or first as end
        if second_cave == "start" or first_cave == "end":
            first_cave, second_cave = second_cave, first_cave
        if (first_cave.isupper() or second_cave.isupper()) and (first_cave != "start" and second_cave != "end"):
            cave_system.add_edge(first_cave, second_cave)
            cave_system.add_edge(second_cave, first_cave)
        else:
            cave_system.add_edge(first_cave, second_cave)
    return cave_system

def find_all_paths_recursive(network, start, end, paths, path = []):
    path = path + [start]
    # If we reached the end, then add to path 
    if start == end:
        paths.append(path)
    else:
        for node in network[start].keys():
            # If its upper since it can be revisited go again
            if node.isupper():
                find_all_paths_recursive(network, node, end, paths, path = path)
            elif node not in path:
                find_all_paths_recursive(network, node, end, paths, path = path)       

def find_all_paths(network, start, end, paths):
    find_all_paths_recursive(network, start, end, paths)
    

def p2_find_all_paths_recursive(network, start, end, paths, path = (), visited_twice = ''):
    path = path + (start,)
    if visited_twice == '':
        for node in network.nodes:
            if not node.isupper() and path.count(node) == 2:
                visited_twice = node
    # If we reached the end, then add to path 
    if start == end:
        paths.add(path)
    else:
        for node in network[start].keys():
            # If its upper since it can be revisited go again
            if node == 'start' or (node == visited_twice):
                continue
            elif node.isupper() or visited_twice == '':
                p2_find_all_paths_recursive(network, node, end, paths, path = path, visited_twice = visited_twice)
            elif visited_twice != '' and node not in path:
                p2_find_all_paths_recursive(network, node, end, paths, path = path, visited_twice = visited_twice) 
                  

def p2_find_all_paths(network, start, end, paths):
    p2_find_all_paths_recursive(network, start, end, paths)



if __name__ == "__main__":
    # Test 1
    test_1 = create_network('test-1.txt')
    paths = []
    find_all_paths(test_1, 'start', 'end', paths)
    assert len(paths) == 10
    # Test 2
    test_2 = create_network('test-2.txt')
    paths = []
    find_all_paths(test_2, 'start', 'end', paths)
    assert len(paths) == 19
    # Test 3
    test_3 = create_network('test-3.txt')
    paths = []
    find_all_paths(test_3, 'start', 'end', paths)
    assert len(paths) == 226
    # Part 1
    paths = []
    input_network = create_network('input.txt')
    paths = []
    find_all_paths(input_network, 'start', 'end', paths)
    print('Answer to Part 1: {}'.format(len(paths)))
    # Second part test 1
    paths = set()
    p2_find_all_paths(test_1, 'start', 'end', paths)
    assert len(paths) == 36
    # Second part test 2
    paths = set()
    p2_find_all_paths(test_2, 'start', 'end', paths)
    assert len(paths) == 103
    # Second part test 3
    paths = set()
    p2_find_all_paths(test_3, 'start', 'end', paths)
    assert len(paths) == 3509
    # Part 2
    paths = set()
    p2_find_all_paths(input_network, 'start', 'end', paths)
    print('Answer to Part 2: {}'.format(len(paths)))