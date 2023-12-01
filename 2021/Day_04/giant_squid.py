import numpy as np

def bingo_part1(file):
    input = open(file, 'r')
    input = input.read().split('\n')
    input = [line for line in input if line]
    # Get the bingo numbers
    bingo_nums = np.array(input[0].split(','), dtype = np.int64)
    # Format the games
    games = np.array(input[1:])
    games = np.char.split(games)
    # Create bingo games array
    bingo_games = np.zeros((games.size // 5, 5, 5), dtype = int)
    bingos = np.zeros_like(bingo_games)
    game = 0
    game_line = 0
    # Read bingo games into array
    for line in games:
        if game_line == 5:
            game += 1
            game_line = 0
        line = np.array(line, dtype = int)
        bingo_games[game, game_line, :] = line
        game_line += 1
    winner = -1
    winning_num = -1
    for num in bingo_nums:
        bingos[np.where(bingo_games == num)] = 1
        row_sums = np.sum(bingos, axis = 2)
        col_sums = np.sum(bingos, axis = 1)
        if np.any(row_sums == 5) or np.any(col_sums == 5):
            # Get the winner
            winner = np.where((row_sums == 5) | (col_sums == 5))[0][0]
            winning_num = num
            # Break the loop
            break
    winner_game = bingo_games[winner]
    winner_bingo = bingos[winner]
    unmarked_sum = np.sum(winner_game[np.where(winner_bingo == 0)])
    return unmarked_sum * winning_num

def let_the_wookie_win(file):
    input = open(file, 'r')
    input = input.read().split('\n')
    input = [line for line in input if line]
    # Get the bingo numbers
    bingo_nums = np.array(input[0].split(','), dtype = np.int64)
    # Format the games
    games = np.array(input[1:])
    games = np.char.split(games)
    # Create bingo games array
    bingo_games = np.zeros((games.size // 5, 5, 5), dtype = int)
    bingos = np.zeros_like(bingo_games)
    game = 0
    game_line = 0
    # Read bingo games into array
    for line in games:
        if game_line == 5:
            game += 1
            game_line = 0
        line = np.array(line, dtype = int)
        bingo_games[game, game_line, :] = line
        game_line += 1
    # Play Bingo!
    winner_index = -1
    winning_num = -1
    previous_winners = np.array([])
    winner_game = bingo_games[winner_index]
    winner_bingo = bingos[winner_index]
    for num in bingo_nums:
        bingos[np.where(bingo_games == num)] = 1
        row_sums = np.sum(bingos, axis = 2)
        col_sums = np.sum(bingos, axis = 1)
        if np.any(row_sums == 5) or np.any(col_sums == 5):
            # Get the winner
            winner = np.unique(np.where((row_sums == 5) | (col_sums == 5))[0])  
            # Only change the winner game and winner_bingo when a new one is added
            if winner.size > previous_winners.size:
                winning_num = num
                winner_index = winner[np.isin(winner, previous_winners, invert = True)][0]
                winner_game = np.copy(bingo_games[winner_index])
                winner_bingo = np.copy(bingos[winner_index])
                previous_winners = np.unique(winner)
    print(winner_index)
    print(winning_num)
    print(winner_bingo)
    print(winner_game)
    unmarked_sum = np.sum(winner_game[np.where(winner_bingo == 0)])
    return unmarked_sum * winning_num

if __name__ == '__main__':
    print(bingo_part1('input.txt'))
    print(let_the_wookie_win('input.txt'))