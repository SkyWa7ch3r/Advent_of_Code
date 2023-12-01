import numpy as np
import re

def find_intersections(file):
    input = open(file, 'r')
    coords = re.split("->|, |,|\n", input.read().strip())
    coords = np.array(coords, dtype = int)
    coords = coords.reshape((-1, 2, 2))
    shape = np.max(np.max(np.max(coords, axis = 0), axis = 1) + 1)
    sea_floor = np.zeros((shape, shape), dtype = int)
    for i in range(coords.shape[0]):
        coord_1 = coords[i][0]
        coord_2 = coords[i][1]
        if coord_1[0] == coord_2[0] or coord_1[1] == coord_2[1]:
            # If first x is largen the second, swap them
            if coord_1[0] > coord_2[0]:
                coord_1[0], coord_2[0] = coord_2[0], coord_1[0]
            # If first y is larger the second, swap them
            if coord_1[1] > coord_2[1]:
                coord_1[1], coord_2[1] = coord_2[1], coord_1[1]
            sea_floor[coord_1[1] : coord_2[1] + 1, coord_1[0] : coord_2[0] + 1] += 1
    return np.where(sea_floor > 1)[0].size

def find_intersections_and_diags(file):
    input = open(file, 'r')
    coords = re.split("->|, |,|\n", input.read().strip())
    coords = np.array(coords, dtype = int)
    coords = coords.reshape((-1, 2, 2))
    shape = np.max(np.max(np.max(coords, axis = 0), axis = 1) + 1)
    sea_floor = np.zeros((shape, shape), dtype = int)
    print(sea_floor.shape)
    for i in range(coords.shape[0]):
        coord_1 = coords[i][0]
        coord_2 = coords[i][1]
        if coord_1[0] == coord_2[0] or coord_1[1] == coord_2[1]:
            # If first x is largen the second, swap them
            if coord_1[0] > coord_2[0]:
                coord_1[0], coord_2[0] = coord_2[0], coord_1[0]
            # If first y is larger the second, swap them
            if coord_1[1] > coord_2[1]:
                coord_1[1], coord_2[1] = coord_2[1], coord_1[1]
            sea_floor[coord_1[1] : coord_2[1] + 1, coord_1[0] : coord_2[0] + 1] += 1
        elif abs(coord_1[0] - coord_2[0]) == abs(coord_1[1] - coord_2[1]):
            # If first x is larger, doing arange decreasing else increasing
            if coord_1[0] > coord_2[0]:
                x = np.arange(coord_1[0], coord_2[0] - 1, -1)
            else:
                x = np.arange(coord_1[0], coord_2[0] + 1)
            # If first y is larger the second, swap them
            if coord_1[1] > coord_2[1]:
                y = np.arange(coord_1[1], coord_2[1] - 1, -1)
            else:
                y = np.arange(coord_1[1], coord_2[1] + 1)
            sea_floor[(y, x)] += 1
    return np.where(sea_floor > 1)[0].size

def why_not_both(file, diag = False):
    input = open(file, 'r')
    coords = re.split("->|, |,|\n", input.read().strip())
    coords = np.array(coords, dtype = int)
    coords = coords.reshape((-1, 2, 2))
    shape = np.max(np.max(np.max(coords, axis = 0), axis = 1) + 1)
    sea_floor = np.zeros((shape, shape), dtype = int)
    for i in range(coords.shape[0]):
        coord_1 = coords[i][0]
        coord_2 = coords[i][1]
        if coord_1[0] == coord_2[0] or \
            coord_1[1] == coord_2[1] or \
            (abs(coord_1[0] - coord_2[0]) == abs(coord_1[1] - coord_2[1]) and diag):
            # If first x is largen the second, swap them
            if coord_1[0] > coord_2[0]:
                x = np.arange(coord_1[0], coord_2[0] - 1, -1)
            else:
                x = np.arange(coord_1[0], coord_2[0] + 1)
            # If first y is larger the second, swap them
            if coord_1[1] > coord_2[1]:
                y = np.arange(coord_1[1], coord_2[1] - 1, -1)
            else:
                y = np.arange(coord_1[1], coord_2[1] + 1)
            sea_floor[(y, x)] += 1
    return np.where(sea_floor > 1)[0].size

if __name__ == "__main__":
    print(find_intersections('input.txt'))
    print(find_intersections_and_diags('input.txt'))
    print(why_not_both('input.txt'))
    print(why_not_both('input.txt', diag = True))