from urllib.request import urlopen
import numpy as np

def get_increasing(file):
    # Read the file and turn it into a numpy array
    input = np.array(list(open(file, 'r')), dtype = np.int64)
    # Get the differences between the values
    differences = np.diff(input)
    # Return all the differences that were above 0
    return np.sum(differences > 0)

def get_sliding_window_increase(file, window_size = 3):
    # Read the file
    input = np.array(list(open(file, 'r')), dtype = np.int64)
    # Do a convolution on the array with 3 1's as the kernel, set as valid to do no padding.
    # Does mean that the window size must be a factor of the size ideally.
    summed_windows = np.convolve(input, np.ones(window_size, dtype=int),'valid')
    # get the differences
    differences = np.diff(summed_windows)
    # Return the sum of boolean vector of values above zero.
    return np.sum(differences > 0)

if __name__ == '__main__':
    print("The depth increased {} times".format(get_increasing('input.txt')))
    print("Taking into account a sliding window sum, the depth increased {} times".format(get_sliding_window_increase('input.txt')))