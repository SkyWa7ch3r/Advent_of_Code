import cudf as cd
import cupy as cp
import time

def solution():
    input = cd.read_text("input.txt", delimiter='\n', strip_delimiters = True)
    locations = cp.array(input[0].split(':')[1].strip().split(' '), dtype = cp.int64)
    farm = cd.DataFrame(columns=['section', 'start', 'end', 'step'])
    sections = input[2:][input[2:] == ''].index.to_arrow().to_pylist()
    current_index = 2
    current_section = 1 # 1 = soil, 2 = fertilizer, ... 7 = location
    for end_index in sections:
        map = input[current_index : end_index]
        map = map.reset_index(drop = True)
        name = map[0].split('-')[-1].split(' ')[0].strip()
        map = map[1:]
        map = map.str.strip().str.split(' ', expand = True).astype(int).to_cupy()
        location_found = cp.full_like(locations, False)
        for item_start, section_start, step in map:
            mapping = cp.zeros(4, dtype = cp.int64)
            mapping[0] = current_section
            mapping[1] = section_start
            mapping[2] = section_start + step
            mapping[3] = item_start - section_start
            new_section = cd.DataFrame(
                mapping.reshape([1,4]),
                columns=['section', 'start', 'end', 'step']
            )
            for location_index, location in enumerate(locations):
                if (mapping[1] <= location) and (location <= mapping[2]) and not location_found[location_index]:
                    locations[location_index] += mapping[3]
                    location_found[location_index] = True
            farm = cd.concat([farm,new_section])
        current_index = end_index + 1
        current_section += 1
    print(f"The minimum location for the initial seeds is: {cp.min(locations)}")
start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")