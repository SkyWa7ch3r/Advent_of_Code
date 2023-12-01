import numpy as np

def pair_insertion(file, steps):
    """
    Takes in a text file, and uses the firts line as the template.
    Then reads every 2 characters and inserts in between if it matches a subset.
    It does this step times.

    Parameters
    ----------
    file : string
        filename
    steps : int
        Number of steps (iterations the program should go through)

    Returns
    -------
    template
        Updated template from file
    """
    inputs = np.char.strip(np.array(open(file, 'r').readlines()))
    template = list(inputs[0])
    rules = inputs[2:]
    rules = np.array(list(np.char.split(rules, ' -> ')))
    keys = rules[:, 0]
    values = rules[:, 1]
    rules = dict(zip(keys, values))
    new_template = template.copy()
    for i in range(steps):
        replacements = 0
        for i in range(len(template) - 1):
            subset = ''.join(template[i : i + 2])
            if subset in rules:
                new_template.insert(i + 1 + replacements, rules[subset])
                replacements += 1
        template = new_template.copy()
    return template

def scalable_counting(file, steps):
    # Read in the input, extract the relevant parts
    inputs = np.char.strip(np.array(open(file, 'r').readlines()))
    template = list(inputs[0])
    rules = inputs[2:]
    rules = np.array(list(np.char.split(rules, ' -> ')))
    keys = rules[:, 0]
    values = rules[:, 1]
    # Put rules into a dictionary
    rules = dict(zip(keys, values))
    # Setup the dictionary to keep track the combinations
    count_template = dict(zip(keys, np.zeros(len(keys), dtype = np.int64)))
    for i in range(len(template) - 1):
        subset = ''.join(template[i : i + 2])
        if subset in rules:
            count_template[subset] = count_template[subset] + 1
    for i in range(steps):
        current_template = dict(zip(keys, np.zeros(len(keys), dtype = int)))
        # At each step, go through the keys of the current template
        for key in count_template:
            # If the value is not zero
            if count_template[key] != 0:
                # Get the new subset of characters to examine
                string = list(key[0] + rules[key] + key[1])
                # Add to the current values template
                for i in range(len(string) - 1):
                    # Get a subset of the small string (2 characters)
                    subset = ''.join(string[i : i + 2])
                    # If its in the rules, then add the amount of the current_template key as it will occur that many times in the step if we were to loop through
                    if subset in rules:
                        current_template[subset] = current_template[subset] + count_template[key]
        count_template = current_template.copy()
    # Now that we have the counts, extract the letters into a dictionary, then add numbers together
    char_counts = {}
    for key in count_template:
        char_1, char_2 = key[0], key[1]
        if char_1 in char_counts:
            char_counts[char_1] = char_counts[char_1] + count_template[key] / 2
        else:
            char_counts[char_1] = count_template[key] / 2
        if char_2 in char_counts:
            char_counts[char_2] = char_counts[char_2] + count_template[key] / 2
        else:
            char_counts[char_2] = count_template[key] / 2
    char_counts = {key : np.ceil(char_counts[key]) for key in char_counts}
    return char_counts
            




def get_min_max_count_diff(template):
    """
    Takes a template and gets the difference in occurence between most frequent letter
    against the least frequent letter

    Parameters
    ----------
    template : list
        A string as a list
    """
    template = np.array(template)
    keys = set(template)
    values = [0] * len(keys)
    hist = dict(zip(keys, values))
    for char in template:
        hist[char] = hist[char] + 1
    hist = sorted(hist.items(), key=lambda item: item[1], reverse = True)
    return hist[0][1] - hist[-1][1]


if __name__ == '__main__':
    # Part 1 Tests
    assert ''.join(pair_insertion('test.txt', 1)) == 'NCNBCHB'
    assert ''.join(pair_insertion('test.txt', 2)) == 'NBCCNBBBCBHCB'
    assert ''.join(pair_insertion('test.txt', 3)) == 'NBBBCNCCNBBNBNBBCHBHHBCHB'
    assert ''.join(pair_insertion('test.txt', 4)) == 'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'
    assert get_min_max_count_diff(pair_insertion('test.txt', 10)) == 1588
    # Part 1
    input_template = pair_insertion('input.txt', 10)
    print(get_min_max_count_diff(input_template))
    # Part 2 Test
    counts = scalable_counting('test.txt', 40)
    counts = sorted(counts.items(), key=lambda item: item[1], reverse = True)
    assert (counts[0][1] - counts[-1][1]) == 2188189693529
    # Part 2
    counts = scalable_counting('input.txt', 40)
    counts = sorted(counts.items(), key=lambda item: item[1], reverse = True)
    print(counts[0][1] - counts[-1][1])


