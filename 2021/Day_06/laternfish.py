import numpy as np

def count_fish(days, file):
    fish = np.array(open(file, "r").read().split(","), dtype = int)
    fish_to_change = []
    for day in range(days):
        # Change fish to 6
        fish[fish_to_change] = 6
        # Get the number_to_spawn
        number_to_spawn = np.count_nonzero(fish == 0)
        # Change all zeros to 6 
        fish_to_change = np.where(fish <= 0)
        # Take a day off each fish
        fish -= 1
        # Add the fish
        fish = np.pad(fish, number_to_spawn, constant_values = 8)[number_to_spawn:]
    return fish.size

def count_more_fish(days, file):
    fish = np.array(open(file, "r").read().split(","), dtype = int)
    fish_counter = np.zeros(9, dtype = int)
    counted = np.bincount(fish)
    fish_counter[:counted.size] = counted
    for day in range(days):
        fish_counter[7] += fish_counter[0]
        fish_counter = np.roll(fish_counter, -1)
    return np.sum(fish_counter)

if __name__ == "__main__":
    print(count_fish(80, "input.txt"))
    print(count_more_fish(256, 'input.txt'))
