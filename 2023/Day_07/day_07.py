import cudf as cd
import cupy as cp
from functools import cmp_to_key
import time

def compare_hands(a, b):
    label_ranking = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    for idx in range(len(a[1])):
        if label_ranking.index(a[1][idx]) == label_ranking.index(b[1][idx]):
            continue
        elif label_ranking.index(a[1][idx]) < label_ranking.index(b[1][idx]):
            return 1
        else:
            return -1
    return 0

def compare_hands_joker(a, b):
    label_ranking = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
    for idx in range(len(a[1])):
        if label_ranking.index(a[1][idx]) == label_ranking.index(b[1][idx]):
            continue
        elif label_ranking.index(a[1][idx]) < label_ranking.index(b[1][idx]):
            return 1
        else:
            return -1
    return 0


def parse_input():
    input = cd.read_text("input.txt", delimiter = "\n", strip_delimiters = True)
    input = input.str.split(' ', expand = True)
    input.columns = ['hand', 'bid']
    input['rank'] = cp.zeros(input.shape[0], dtype = cp.int64)
    input['bid'] = input['bid'].astype(int)
    return input

def solution_1(input):
    ranks = cp.arange(input.shape[0]) + 1
    # Silly me put them in descending order had to reverse to do what I'm thinking
    keys = ['five_of_a_kind', 'four_of_a_kind', 'full_house', 'three_of_a_kind', 'two_pair', 'pair', 'high'][::-1]
    hand_types = {key: [] for key in keys}
    hands = input['hand'].to_arrow().to_pylist()
    for idx, hand in enumerate(hands):
        hand_tokens = {i: hand.count(i) for i in set(hand)}
        labels = list(dict(sorted(hand_tokens.items(), key=lambda item: item[1])[::-1]).keys())
        if hand_tokens[labels[0]] == 5:
            hand_types['five_of_a_kind'].append((idx, hand))
        elif hand_tokens[labels[0]] == 4:
            hand_types['four_of_a_kind'].append((idx, hand))
        elif len(labels) == 2 and hand_tokens[labels[0]] == 3 and hand_tokens[labels[1]] == 2:
            hand_types['full_house'].append((idx, hand))
        elif hand_tokens[labels[0]] == 3:
            hand_types['three_of_a_kind'].append((idx, hand))
        elif len(labels) == 3 and hand_tokens[labels[0]] == 2 and hand_tokens[labels[1]] == 2:
            hand_types['two_pair'].append((idx, hand))
        elif hand_tokens[labels[0]] == 2:
            hand_types['pair'].append((idx, hand))
        else:
            hand_types['high'].append((idx, hand))
    rank_order = []
    for key in keys:
        idxs = [hand[0] for hand in sorted(hand_types[key], key = cmp_to_key(compare_hands), reverse = True)]
        rank_order += idxs
    input['rank'][rank_order] = ranks
    print(f"The total winnings for your hands are {(input['bid'] * input['rank']).sum()}")

def solution_2(input):
    ranks = cp.arange(input.shape[0]) + 1
    # Silly me put them in descending order had to reverse to do what I'm thinking
    keys = ['five_of_a_kind', 'four_of_a_kind', 'full_house', 'three_of_a_kind', 'two_pair', 'pair', 'high'][::-1]
    hand_types = {key: [] for key in keys}
    hands = input['hand'].to_arrow().to_pylist()
    for idx, hand in enumerate(hands):
        hand_tokens = {i: hand.count(i) for i in set(hand)}
        labels = list(dict(sorted(hand_tokens.items(), key=lambda item: item[1])[::-1]).keys())
        if 'J' in labels and len(labels) != 1:
            labels.remove('J')
        if hand_tokens[labels[0]] == 5 or ('J' in hand and ((hand_tokens[labels[0]] + hand_tokens['J']) == 5)):
            hand_types['five_of_a_kind'].append((idx, hand))
        elif hand_tokens[labels[0]] == 4 or ('J' in hand and ((hand_tokens[labels[0]] + hand_tokens['J']) == 4)):
            hand_types['four_of_a_kind'].append((idx, hand))
        elif (len(labels) == 2 and hand_tokens[labels[0]] == 3 and hand_tokens[labels[1]] == 2) or \
            ('J' in hand and len(labels) == 2 and (hand_tokens[labels[0]] + hand_tokens[labels[1]] + hand_tokens['J']) == 5):
            hand_types['full_house'].append((idx, hand))
        elif hand_tokens[labels[0]] == 3 or ('J' in hand and len(labels) == 3 and (hand_tokens[labels[0]] + hand_tokens['J']) == 3):
            hand_types['three_of_a_kind'].append((idx, hand))
        # Two pair with a J is impossible with 5 labels
        elif len(labels) == 3 and hand_tokens[labels[0]] == 2 and hand_tokens[labels[1]] == 2:
            hand_types['two_pair'].append((idx, hand))
        elif hand_tokens[labels[0]] == 2 or ('J' in hand and len(labels) == 4):
            hand_types['pair'].append((idx, hand))
        else:
            hand_types['high'].append((idx, hand))
    rank_order = []
    for key in keys:
        idxs = [hand[0] for hand in sorted(hand_types[key], key = cmp_to_key(compare_hands_joker), reverse = True)]
        rank_order += idxs
    input['rank'][rank_order] = ranks
    print(f"The total winnings for your hands are with the joker rule {(input['bid'] * input['rank']).sum()}")

start = time.time()
input = parse_input()
solution_1(input)
solution_2(input)
end = time.time()
print(f"{round(end - start, 3)} seconds")