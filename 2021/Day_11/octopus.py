import numpy as np
from scipy.ndimage import minimum_filter, maximum_filter

def octopi_p1(file, steps):
    # Extract Input
    inputs = open(file, 'r').readlines()
    length = len(inputs)
    shape = (length, len(inputs[0].strip()))
    octopi = np.zeros(shape, dtype = int)
    for i in range(length):
        octopi[i] = np.array(list(inputs[i].strip()), dtype = int)
    # Setup the loop
    previous = octopi
    flashes = 0
    # Footprint for the filter
    footprint = [[1,1,1],[1,0,1],[1,1,1]]
    # For every step
    for i in range(steps):
        octopi += 1
        change = True
        flashed = np.zeros_like(octopi)
        # While the octopi array changes
        while change:
            # Get over 9s and setup the filter
            over_9s = np.where(octopi > 9)
            filter = np.zeros_like(octopi, dtype = int)
            # For every over 9, add 1 to surrounding places in filter
            for row, col in zip(*over_9s):
                # Setup the chnage to add to the filter
                zeros = np.zeros_like(octopi, dtype = int)
                zeros[row, col] = 1
                flashed[row, col] = 1
                # Change the filter
                filter = filter + maximum_filter(zeros, footprint = footprint)
                # Set all values over 9 to zero in the filter
                filter[over_9s] = 0
            # Now the filter has considered every 9, add it to octopi
            octopi = octopi + filter
            # Change all flashed to 0, can only flash once
            octopi[flashed == 1] = 0
            # If the filter didnt change anything, stop the loop
            if np.array_equal(octopi, previous):
                change = False
            # Else keep the loop going
            else:
                previous = octopi
        # Now we have the amount that flashed in this step, add them to the flashes
        flashes += np.sum(flashed)
    return flashes

def octopi_p2(file):
        # Extract Input
    inputs = open(file, 'r').readlines()
    length = len(inputs)
    shape = (length, len(inputs[0].strip()))
    octopi = np.zeros(shape, dtype = int)
    for i in range(length):
        octopi[i] = np.array(list(inputs[i].strip()), dtype = int)
    # Setup the loop
    previous = octopi
    flashes = 0
    # Footprint for the filter
    footprint = [[1,1,1],[1,0,1],[1,1,1]]
    step = 1
    # For every step
    while True:
        octopi += 1
        change = True
        flashed = np.zeros_like(octopi)
        # While the octopi array changes
        while change:
            # Get over 9s and setup the filter
            over_9s = np.where(octopi > 9)
            filter = np.zeros_like(octopi, dtype = int)
            # For every over 9, add 1 to surrounding places in filter
            for row, col in zip(*over_9s):
                # Setup the chnage to add to the filter
                zeros = np.zeros_like(octopi, dtype = int)
                zeros[row, col] = 1
                flashed[row, col] = 1
                # Change the filter
                filter = filter + maximum_filter(zeros, footprint = footprint)
                # Set all values over 9 to zero in the filter
                filter[over_9s] = 0
            # Now the filter has considered every 9, add it to octopi
            octopi = octopi + filter
            # Change all flashed to 0, can only flash once
            octopi[flashed == 1] = 0
            # If the filter didnt change anything, stop the loop
            if np.array_equal(octopi, previous):
                change = False
            # Else keep the loop going
            else:
                previous = octopi
        # Now we have the amount that flashed in this step, add them to the flashes
        if np.sum(flashed) == flashed.size:
            break
        step += 1
    return step


print(octopi_p1('input.txt', 100))
print(octopi_p2('input.txt'))