import cudf as cd
import numpy as np
import time

def parse_input():
    input = cd.read_text("input.txt", delimiter='\n', strip_delimiters = True)
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
                if (section_start <= location) and (location < (section_start + num_range)):
                    location = item_start + (location - section_start)
                    break
        if minimum_location > location:
            minimum_location = location
    print(f"The minimum location for the initial seeds is: {minimum_location}")

def solution_2(seeds, maps):
    lengths = seeds[1::2]
    seeds = seeds[0::2]
    minimum_location = np.iinfo(np.int64).max - 1
    for seed, length in zip(seeds, lengths):
        locations = [[seed, seed + length - 1]]
        for map in maps:
            location_i = 0
            while location_i < len(locations):
                loc_start = locations[location_i][0]
                loc_end = locations[location_i][1]
                for item, section, num_range in map:
                    if (item == 0 and section == 0 and num_range == 0):
                        break
                    if section <= locations[location_i][0] and section + num_range > locations[location_i][0]:
                        if loc_end < section + num_range:
                            locations[location_i][0] = item + loc_start - section
                            locations[location_i][1] = item + loc_end - section
                            break
                        elif loc_end >= section + num_range:
                            locations[location_i][0] = item + loc_start - section
                            locations[location_i][1] = item + section + num_range - 1 - section
                            locations.append([section + num_range, loc_end])
                            break
                location_i += 1
        current_min_location = np.min(np.array(locations)[:, 0])
        if minimum_location > current_min_location:
            minimum_location = current_min_location
    print(f"The minimum location for the initial seeds is: {minimum_location}")
   

start = time.time()
seeds, maps = parse_input()
solution_1(seeds, maps)
solution_2(seeds, maps)
end = time.time()
print(f"{round(end - start, 3)} seconds")