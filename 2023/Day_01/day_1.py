import cudf as cd
import pandas as pd
import time

def solution_1():
    input = cd.read_text("input.txt", delimiter="\n", strip_delimiters=True)
    numbers = input.str.findall(r'[0-9]')
    numbers = numbers.list.get(0) + numbers.list.get(-1)
    numbers = numbers.astype(int)
    return numbers.sum()

def solution_2():
    replacement = {
        'one' : 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }
    input = pd.read_csv("input.txt",header = None)[0]
    # Wouldn't have to do this in pandas dumb replace if the regex (?=(one|two|three|four|five|six|seven|eight|nine|[0-9]) would work in cudf for some reason it doesn't
    # but it still works under 1 second
    numbers = input.str.findall(r'(?=(one|two|three|four|five|six|seven|eight|nine|[0-9]))')
    numbers = numbers.apply(lambda x: str(replacement[x[0]] if x[0] in replacement else x[0]) + str(replacement[x[-1]] if x[-1] in replacement else x[-1]))
    numbers = numbers.astype(int)
    return numbers.sum()

start = time.time()
print(f"Solution 1: Sum of the calibration values: {solution_1()}")
print(f"Solution 2: Sum of the calibration values: {solution_2()}")
end = time.time()
print(f"{round(end - start, 3)} seconds")

