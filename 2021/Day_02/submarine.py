import numpy as np

def submarine(file):
    input = open(file, 'r')
    # horizontal, depth, aim
    coord = np.zeros(3)
    for line in input:
        split_line = line.split()
        if split_line[0] == "forward":
            coord[0] += int(split_line[1])
            coord[1] += int(split_line[1]) * coord[2]
        elif split_line[0] == "down":
            coord[2] += int(split_line[1])
        elif split_line[0] == "up":
            coord[2] -= int(split_line[1])
    return coord

if __name__ == '__main__':
    coord = submarine("input.txt")
    print(coord)
    print(coord[0] * coord[1])