import cudf as cd
import cupy as cp
import time

def solution():
    input = cd.read_text("input.txt", delimiter = "\n", strip_delimiters = True)
    input = input.str.split(':').list.get(1).str.strip()
    part1_input = input.str.split('', expand = True).astype(int)
    times_distances = part1_input.to_cupy().transpose()
    ways_to_win = 1
    for time, distance in times_distances:
        hold_times = cp.arange(time + 1)
        ways_to_win *= cp.sum((hold_times * (hold_times.size - 1 - hold_times) - distance) > 0)
    print(f"The number of ways to win is: {ways_to_win}")
    part2_input = input.str.replace("\s+", "").astype(int).to_cupy().transpose()
    hold_times = cp.arange(part2_input[0] + 1)
    beat_record = cp.sum((hold_times * (hold_times.size - 1 - hold_times) - part2_input[1]) > 0)
    print(f"The number of ways to win in the one race is: {beat_record}")
    

start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")
    
