import cudf as cd
import cupy as cp
import time

def solution():
    input = cd.read_text("test.txt", delimiter='\n', strip_delimiters = True)
    seeds = cp.array(input[0].split(':')[1].strip().split(' '), dtype = cp.int64)
    farm = cd.DataFrame(columns=['seed_low', 'seed_high'])
    sections = input[2:][input[2:] == ''].index.to_arrow().to_pylist()
    current_index = 2
    current_section = 'seed'
    end_index = 5
    map = input[current_index : end_index]
    map = map.reset_index(drop = True)
    name = map[0].split('-')[-1].split(' ')[0].strip()
    map = map[1:]
    map = map.str.strip().str.split(' ', expand = True).astype(int).to_cupy()
    item_indexes = cp.zeros([map.shape[0], 2])
    section_indexes = cp.zeros([map.shape[0], 2])
    for idx, (item, section, step) in enumerate(map):
        item_indexes[idx, 0] = item
        item_indexes[idx, 1] = item + step -1
        section_indexes[idx, 0] = section
        section_indexes[idx, 1] = section + step - 1
    item_min = cp.min(item_indexes)
    section_min = cp.min(section_indexes)
    if item_min != 0:
        item_indexes = cp.append(item_indexes, 0)
        item_indexes = cp.append(item_indexes, item_min - 1).reshape([map.shape[0] + 1, 2])
        item_indexes = cp.reshape(item_indexes, [map.shape[0] + 1, 2])
    if section_min != 0:
        section_indexes = cp.append(section_indexes, 0)
        section_indexes = cp.append(section_indexes, section_min - 1)
        section_indexes = cp.reshape(section_indexes, [map.shape[0] + 1, 2])
    if cp.max(item_indexes) >= cp.max(section_indexes):
        sorted_indexes = cp.argsort(item_indexes[:, 0])
    else:
        sorted_indexes = cp.argsort(section_indexes[:, 0])
    print(item_indexes[sorted_indexes, :])
    print(section_indexes[sorted_indexes, :])
    print(sorted_indexes)
    current_index = end_index + 1
    current_section = name

start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")