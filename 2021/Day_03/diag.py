import numpy as np

def part_1(file):
    input = list(open(file, 'r'))
    ones = np.zeros(len(input[0].strip()), dtype = int)
    zeros = np.zeros(len(input[0].strip()), dtype = int)
    for line in input:
        binary = np.array(list(line.strip()), dtype = int)
        ones += binary
        inverted = np.invert(binary.astype(bool)).astype(int)
        zeros += inverted
    gamma = ""
    epsilon = ""
    for one, zero in zip(ones, zeros):
        if one >= zero:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    power = int(gamma, 2) * int(epsilon, 2)
    return power

def part_2(file):
    input = np.array(list(open(file, 'r')))
    input = np.char.strip(input)
    oxygen = input
    co2 = input
    for i in range(len(input[0])):
        oxy_ones = 0
        oxy_zeros = 0
        co2_ones = 0
        co2_zeros = 0
        for oxy_l in oxygen:
            # Do oxygen
            binary = np.array(list(oxy_l), dtype = int)
            if binary[i] == 1:
                oxy_ones += 1
            else:
                oxy_zeros += 1
        for co2_l in co2:
            # Do the co2
            binary = np.array(list(co2_l), dtype = int)
            if binary[i] == 1:
                co2_ones += 1
            else:
                co2_zeros += 1

        # Check for oxygen which looks for largest
        if oxygen.size > 1:
            if oxy_ones >= oxy_zeros:
                oxygen = oxygen[np.nonzero(np.char.find(oxygen, '1', i, i + 1) == i)]
            else:
                oxygen = oxygen[np.nonzero(np.char.find(oxygen, '0', i, i + 1) == i)]
        # Check for co2 which looks for smallest
        if co2.size > 1:
            if co2_ones >= co2_zeros:
                co2 = co2[np.nonzero(np.char.find(co2, '0', i, i + 1) == i)]
            else:
                co2 = co2[np.nonzero(np.char.find(co2, '1', i, i + 1) == i)]
    oxygen = oxygen[0]
    co2 = co2[0]
    life_support = int(oxygen, 2) * int(co2, 2)
    return life_support
    



if __name__ == '__main__':
    print(part_1('input.txt'))
    print(part_2('input.txt'))

    