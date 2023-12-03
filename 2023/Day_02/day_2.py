import cudf as cd
import time


def get_ball_max(color):
    if color == 'red':
        return 12
    elif color == 'green':
        return 13
    else:
        return 14


def solution():
    input = cd.read_text("input.txt", delimiter="\n", strip_delimiters=True)
    games = input.str.partition(':').loc[:, [0,2]]
    games[0] = games[0].str.split(' ').list.get(-1)
    games[2] = games[2].str.split(';')
    games = games.explode(2)
    games[2] = games[2].str.split(',')
    games = games.explode(2)
    games[2] = games[2].str.strip()
    games['number_of_balls'] = games[2].str.split(' ').list.get(0).astype(int)
    games['color'] = games[2].str.split(' ').list.get(1)
    games['game'] = games[0]
    del[games[0], games[2]]
    games.reset_index(inplace = True, drop = True)
    games['max_balls'] = games['color'].apply(get_ball_max)
    games['possible'] = games['max_balls'] - games['number_of_balls']
    possible_games = games.loc[:, ['game', 'possible']].groupby('game').min()
    possible_mask = possible_games['possible'] >= 0
    print(f"Solution 1: Sum of the calibration values: {possible_games[possible_mask].index.astype(int).sum()}")
    color_games = games.loc[:, ['game', 'color', 'number_of_balls']].groupby(['game', 'color'])
    print(f"Solution 2: Sum of the calibration values: {color_games.max().sort_index().reset_index().groupby('game').prod().sum()[0]}")

start = time.time()
solution()
end = time.time()
print(f"{round(end - start, 3)} seconds")