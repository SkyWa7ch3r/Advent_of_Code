import re
import numpy as np

def syntax(file, error = True):
    # Scores for error characters
    score_dict = {')' : 3, ']' : 57, '}' : 1197, '>' : 25137}
    # Use the opposite of autocomplete characters for scoring
    autocomplete_dict = {'(' : 1, '[' : 2, '{' : 3, '<' : 4}
    program = open(file, 'r').readlines()
    if error:
        score = 0
    else:
        score = []
    for line in program:
        # Remove all instances where things open and close next to each other
        no_change = False
        previous_string = line.strip()
        string_to_check = ''
        # Could have done this recursively, this was easier for me to read at the time
        while not no_change:
            line_subbed= re.sub('<>|\[\]|\(\)|\{\}', '', previous_string)
            if line_subbed == previous_string:
                no_change = True
                string_to_check = line_subbed
            else:
                previous_string = line_subbed
        # Search for the illegals
        matches = re.search('>|\}|\]|\)', string_to_check)
        # If we found one a match and we are looking for errors, take the first illegal and add to score
        if matches is not None and error:
            score += score_dict[matches[0]]
        # Otherwise we are looking to autocomplete the unfinished lines
        elif matches is None and not error:
            string_to_check = string_to_check[::-1]
            line_score = 0
            for character in string_to_check:
                line_score = (line_score * 5) + autocomplete_dict[character]
            score.append(line_score)
    if not error:
        return int(np.median(np.sort(np.array(score))))
    else:
        return score

                

print(syntax('input.txt'))
print(syntax('input.txt', error = False))