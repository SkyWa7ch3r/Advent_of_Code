import cudf as cd
import cupy as cp
from cupyx.scipy.ndimage import label
import time

def solution():
    input = cd.read_text("input.txt", delimiter="")
    line_length = len(cd.read_text("input.txt", delimiter="\n", strip_delimiters = True)[0])
    input = input[input != '\n']
    input = input.reset_index(drop = True)
    input = input.str.replace('.', -3)
    input = input.str.replace('[^a-Z0-9-]|^[-]$',-2)
    input = input.astype(float).to_cupy(dtype = cp.float64)
    input = cp.reshape(input, (input.size // line_length, line_length))
    interesting_indexes = cp.where(input == -2)
    input[input == 0] = -1
    input[input == -3] = 0
    labels = label(input, structure=cp.ones(9).reshape((3,3)))
    n_labels = labels[1]
    labels = labels[0]
    for label_id in range(1, n_labels + 1):
        current_labels = cp.where(labels == label_id)
        if cp.min(input[current_labels]) >= -1:
            labels[current_labels] = 0
    weights = cp.minimum(labels, 1)
    input[interesting_indexes] = 0
    input = input * weights
    number_groups = label(input, structure=cp.ones(9).reshape((3,3)))
    input[input == -1] = 0
    group_sum = 0
    for number_group in range(1, number_groups[1] + 1):
        indexes = cp.where(number_groups[0] == number_group)
        num_gen = 10 ** cp.flip(cp.arange(indexes[0].size))
        group_sum += cp.sum(input[indexes] * num_gen)
    print(f"Solution 1: Sum of the group values: {group_sum}")

start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")