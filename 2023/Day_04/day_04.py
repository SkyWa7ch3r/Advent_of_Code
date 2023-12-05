import cudf as cd
import cupy as cp
import time

def solution():
    input = cd.read_text("input.txt", delimiter="\n", strip_delimiters = True)
    input = input.str.split(':').list.get(1).str.split('|')
    winning_nums = input.list.get(0).str.strip().str.split(expand=True).astype(int).to_cupy()
    cards = input.list.get(1).str.strip().str.split(expand=True).astype(int).to_cupy()
    copies = cp.ones(winning_nums.shape[0], dtype = cp.int64)
    points = cp.zeros(winning_nums.shape[0], dtype = cp.int64)
    for idx in range(winning_nums.shape[0]):
        found_numbers = cp.sum(cp.in1d(winning_nums[idx], cards[idx]))
        copies[idx + 1: idx + found_numbers + 1] += copies[idx]
        points[idx] = 2 ** (found_numbers - 1)
    print(f"The number of points gotten from the cards are: {cp.sum(points)}")
    print(f"The number of scratchcards gotten from the cards are: {cp.sum(copies)}")

start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")