import numpy as np
from scipy.ndimage import label

def minimas(file):
    inputs = open(file, "r").readlines()
    heights = np.zeros((len(inputs), len(inputs[0].strip())), dtype = int)
    for i in range(len(inputs)):
        height = np.array(list(inputs[i].strip()), dtype = int)
        heights[i, :] = height
    minimums = []
    for i in range(heights.shape[0]):
        current_row = heights[i]
        top_i = i - 1
        bot_i = i + 1
        if i == 0:
            top = np.full(current_row.size, 10)
        else: 
            top = heights[top_i]
        if i == heights.shape[0] - 1:
            bot = np.full(current_row.size, 10)
        else:
            bot = heights[bot_i]
        right = np.roll(current_row, -1)
        left = np.roll(current_row, 1)
        right[-1] = 10
        left[0] = 10
        minimas = current_row[np.where((current_row < top) & (current_row < bot) & (current_row < left) & (current_row < right))]
        minimums += list(minimas)
    return np.sum(np.array(minimums) + 1)

def basins(file):
    inputs = open(file, "r").readlines()
    heights = np.zeros((len(inputs), len(inputs[0].strip())), dtype = float)
    for i in range(len(inputs)):
        height = np.array(list(inputs[i].strip()), dtype = float)
        heights[i, :] = height
    # This gives us 1's where there are no 9's
    not_9s = (heights < 9).astype(int)
    # 
    labels, _ = label(not_9s)
    hist = np.bincount(labels.flatten())[1:]
    hist = np.sort(hist)[::-1]
    return np.prod(hist[:3])

print(minimas('input.txt'))
print(basins('input.txt'))
