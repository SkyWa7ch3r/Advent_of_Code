import cudf as cd
import cupy as cp
import time

def solution():
    input = cd.read_text('input.txt', delimiter = '\n', strip_delimiters = True)
    input = input.str.split('', expand = True).astype(int).to_cupy()
    oasis_sum_pt1 = 0
    oasis_sum_pt2 = 0
    for idx in range(input.shape[0]):
        end_diff = input[idx, :][-1]
        start_diffs = []
        diff = input[idx, :]
        while cp.count_nonzero(diff) != 0:
            diff = cp.diff(diff)
            end_diff += diff[-1]
            start_diffs.append(diff)
        oasis_sum_pt1 += end_diff
        start_diff = 0
        for diff in start_diffs[::-1][1:]:
            start_diff = diff[0] - start_diff
        oasis_sum_pt2 += input[idx, 0] - start_diff
    print(f"The extrapolated oasis values sum filling in the last value is: {oasis_sum_pt1}")
    print(f"The extrapolated oasis values sum filling in the first value is: {oasis_sum_pt2}")
start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")