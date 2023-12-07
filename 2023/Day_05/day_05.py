import cudf as cd
import cupy as cp
import time

def solution():
    input = cd.read_text("input.txt", delimiter='\n', strip_delimiters = True)
    seeds = cp.array(input[0].split(':')[1].strip().split(' '), dtype = cp.int64)
    sections = input[2:][input[2:] == ''].index.to_arrow().to_pylist()
    sections.append(input.shape[0])
    current_index = 2
    current_section = 1 # 1 = soil, 2 = fertilizer, ... 7 = location
    maps = []
    for end_index in sections:
        map = input[current_index : end_index]
        map = map.reset_index(drop = True)
        map = map[1:]
        map = map.str.strip().str.split(' ', expand = True).astype(int).to_cupy()
        maps.append(map)
        current_index = end_index + 1
        current_section += 1
    minimum_location = cp.inf
    for seed in seeds:
        location = seed
        for map in maps:
            for item_start, section_start, num_range in map:
                if (section_start <= location) and (location <= (section_start + num_range)):
                    location = item_start + (location - section_start)
                    break
        if minimum_location > location:
            minimum_location = location
    print(f"The minimum location for the initial seeds is: {minimum_location}")
start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")