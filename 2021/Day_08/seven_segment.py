import numpy as np

def seven_segment_p1(file):
    displays = np.array(open(file, "r").readlines())
    digits = np.zeros(10, dtype = int)
    for display in displays:
        output = np.array((display.split(" | ")[1].split()))
        lengths = np.char.str_len(output)
        digits[1] += np.sum(np.count_nonzero(lengths == 2))
        digits[4] += np.sum(np.count_nonzero(lengths == 4))
        digits[7] += np.sum(np.count_nonzero(lengths == 3))
        digits[8] += np.sum(np.count_nonzero(lengths == 7))
    # Keep only 1, 4, 7, 8
    digits = digits[np.nonzero(digits)]
    return np.sum(digits)

def seven_segment_p2(file):
    displays = open(file, "r").readlines()
    digits_chars = {i: set() for i in range(10)}
    output_sum = 0
    for display in displays:
        input = np.array(display.split(' | ')[0].split())
        output = display.split(' | ')[1].split()
        # Get the segments we know 1, 4, 7, 8
        input_lengths = np.char.str_len(input)
        one = set(str(input[np.nonzero(input_lengths == 2)][0]))
        four = set(str(input[np.nonzero(input_lengths == 4)][0]))
        seven = set(str(input[np.nonzero(input_lengths == 3)][0]))
        eight = set(str(input[np.nonzero(input_lengths == 7)][0]))
        output_num = ''
        for seg in output:
            seg = set(seg)
            length = len(seg)
            number = "{}{}{}{}{}".format(len(seg.difference(one)), len(seg.difference(seven)), len(seg.difference(four)),len(eight.difference(seg)), length)
            # Check 1
            if length == 2:
                output_num += '1'
            # Check 4
            elif length == 4:
                output_num += '4'
            # Check 7
            elif length == 3:
                output_num += '7'
            # Check 8
            elif length == 7:
                output_num += '8'
            # Check 0
            elif one.issubset(seg) and seven.issubset(seg) and len(seg.difference(four)) == 3 and len(eight.difference(seg)) == 1 and length == 6:
                print('0 ', number)
                output_num += '0'
            # Check 2
            elif len(seg.difference(one)) == 4 and len(seg.difference(seven)) == 3 and len(seg.difference(four)) == 3 and len(eight.difference(seg)) == 2 and length == 5:
                print('2 ', number)
                output_num += '2'
            # Check 3
            elif one.issubset(seg) and seven.issubset(seg) and len(seg.difference(four)) == 2 and len(eight.difference(seg)) == 2 and length == 5:
                print('3 ', number)
                output_num += '3'
            # Check 5
            elif len(seg.difference(one)) == 4 and len(seg.difference(seven)) == 3 and len(seg.difference(four)) == 2 and len(eight.difference(seg)) == 2 and length == 5:
                print('5 ', number)
                output_num += '5'
            # Check 6
            elif len(seg.difference(one)) == 5 and len(seg.difference(seven)) == 4 and len(seg.difference(four)) == 3 and len(eight.difference(seg)) == 1 and length == 6:
                print('6 ', number)
                output_num += '6'
            # Check 9
            elif one.issubset(seg) and seven.issubset(seg) and four.issubset(seg) and len(eight.difference(seg)) == 1 and length == 6:
                print('9 ', number)
                output_num += '9'
        print(output_num)
        output_sum += int(output_num)
    
    return output_sum

print(seven_segment_p1('input.txt'))

print(seven_segment_p2('input.txt'))
