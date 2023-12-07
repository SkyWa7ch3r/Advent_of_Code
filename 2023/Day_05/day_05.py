import cudf as cd
import numpy as np
from numba import cuda
import time

@cuda.jit()
def find_minimum_location(seed, length, maps, min_location):
    seed_idx = cuda.grid(1)
    if seed_idx < length:
        location = seed_idx + seed
        for maps_idx in range(maps.shape[0]):
            for map_idx in range(maps[maps_idx].shape[0]):
                item_start = maps[maps_idx, map_idx, 0] 
                section_start = maps[maps_idx, map_idx, 1] 
                num_range = maps[maps_idx, map_idx, 2] 
                if item_start != 0 and section_start !=0 and num_range != 0:
                    if (section_start <= location) and (location <= (section_start + num_range)):
                        location = item_start + (location - section_start)
        cuda.atomic.min(min_location, 0, location)

def parse_input():
    input = cd.read_text("test.txt", delimiter='\n', strip_delimiters = True)
    seeds = np.array(input[0].split(':')[1].strip().split(' '), dtype = np.int64)
    sections = cd.Series(input[2:][input[2:] == ''].index)
    map_rows = (sections.diff() - 2).max()
    sections = sections.to_arrow().to_pylist()
    sections.append(input.shape[0])
    current_index = 2
    current_section = 1 # 1 = soil, 2 = fertilizer, ... 7 = location
    maps = np.zeros([len(sections), map_rows, 3], dtype = np.int64)
    for map_idx, end_index in enumerate(sections):
        map = input[current_index : end_index]
        map = map.reset_index(drop = True)
        map = map[1:]
        map = map.str.strip().str.split(' ', expand = True).astype(int).to_numpy()
        maps[map_idx, : map.shape[0], :] = map
        current_index = end_index + 1
        current_section += 1
    return seeds, maps

def solution_1(seeds, maps):
    minimum_location = np.iinfo(np.int64).max 
    for seed in seeds:
        location = seed
        for map in maps:
            for item_start, section_start, num_range in map:
                if (item_start == 0 and section_start == 0 and num_range == 0):
                    break
                if (section_start <= location) and (location <= (section_start + num_range)):
                    location = item_start + (location - section_start)
                    break
        if minimum_location > location:
            minimum_location = location
    print(f"The minimum location for the initial seeds is: {minimum_location}")

def solution_2(seeds, maps):
    # Set minimum value to a functional infinity here (max of int64 - 1)
    minimum_location = cuda.to_device(np.array([np.iinfo(np.int64).max - 1], dtype = np.int64))
    maps = cuda.to_device(np.array(maps, dtype = np.int64))
    lengths = seeds[1::2]
    seeds = seeds[0::2]
    for seed, length in zip(seeds, lengths):
        threads = 1024
        blocks = (length + threads) // threads
        find_minimum_location[blocks, threads](seed, length, maps, minimum_location)
    print(minimum_location.copy_to_host()[0])

start = time.time()
seeds, maps = parse_input()
solution_1(seeds, maps)
solution_2(seeds, maps)
end = time.time()
print(f"{round(end - start, 3)} seconds")