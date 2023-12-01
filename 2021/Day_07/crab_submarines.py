import numpy as np

'''
Crabs only move horizontally
Expends 1 fuel for every movement horizontally

'''

def crab_sub_p1(file):
    crabs = np.array(open(file, "r").read().split(","), dtype = int)
    minimum = np.inf
    for i in range(crabs.size):
        check_min = np.sum(np.abs(crabs - i))
        if check_min < minimum:
            minimum = check_min
            minimum_i = i
    print(np.median(crabs))
    print(minimum_i)
    return minimum

'''
Crabs only move horizontally
Expends more fuel for every movement horizontally

'''

def crab_sub_p2(file):
    crabs = np.array(open(file, "r").read().split(","), dtype = int)
    minimum = np.inf
    arange_sum = lambda x: np.sum(np.arange(x))
    v_arange_sum = np.vectorize(arange_sum)
    for i in range(crabs.size):
        check_min = np.abs(crabs - i)
        check_min = np.sum(v_arange_sum(check_min + 1))
        if check_min < minimum:
            minimum = check_min
    return minimum

'''
Faster thanks to a suggestion from Paul Hancock
'''

def crab_sub_p2_faster(file):
    crabs = np.array(open(file, "r").read().split(","), dtype = int)
    minimum = np.inf
    minimum_i = -1
    arange_sum = lambda x: x*(x+1)/2
    v_arange_sum = np.vectorize(arange_sum)
    for i in range(crabs.size):
        check_min = np.abs(crabs - i)
        check_min = np.sum(v_arange_sum(check_min + 1))
        if check_min < minimum:
            minimum_i = i
            minimum = check_min
    print(np.mean(crabs))
    print(minimum_i)
    return minimum

print(crab_sub_p1('input.txt'))
# print(crab_sub_p2('input.txt'))
print(crab_sub_p2_faster('input.txt'))