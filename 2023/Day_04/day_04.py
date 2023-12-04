import cudf as cd
import cupy as cp
from numba import cuda
import time

# TODO switch to the using numba
@cuda.jit
def get_solution(winning_nums, cards, copies):
    points = 0
    winning, card = cuda.grid(4)
    if winning < winning_nums:
        if card < ca

def solution():
    input = cd.read_text("input.txt", delimiter="\n", strip_delimiters = True)
    input = input.str.split(':').list.get(1).str.split('|')
    winning_nums = input.list.get(0).str.strip().str.split(expand=True).astype(int).to_cupy()
    cards = input.list.get(1).str.strip().str.split(expand=True).astype(int).to_cupy()
    points = cp.zeros(winning_nums.shape[0])
    for idx in range(winning_nums.shape[0]):
        points[idx] = 2 ** (cp.sum(cp.in1d(winning_nums[idx], cards[idx])) - 1)
    print(cp.sum(points))
    threadsperblock = 64
    blockspergrid = (winning_nums.size + (threadsperblock - 1)) // threadsperblock
    copies = cp.zeros_like(cards.shape[0])
    get_solution[threadsperblock, blockspergrid](winning_nums, cards, copies)

start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")