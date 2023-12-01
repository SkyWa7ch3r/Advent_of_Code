import numpy as np

def fold_once(file):
    inputs = np.char.strip(np.array(open(file, 'r').readlines()))
    blank = np.nonzero(inputs == '')[0][0]
    dots = inputs[:blank]
    instructions = inputs[blank + 1:]
    rows = []
    cols = []
    for dot in dots:
        col, row = dot.split(',')
        cols.append(col)
        rows.append(row)
    rows = np.array(rows, dtype = int)
    cols = np.array(cols, dtype = int)
    row_size = np.max(rows)
    col_size = np.max(cols)
    paper = np.zeros((row_size + 1, col_size + 1))
    paper[(rows, cols)] = 1
    fold_xy, fold_coord = instructions[0].split()[2].split('=')
    fold_coord = int(fold_coord)
    if fold_xy == 'y':
        dots_1 = paper[:fold_coord, :].astype(bool)
        dots_2 = paper[fold_coord + 1:].astype(bool)
        paper = dots_1 + np.flipud(dots_2)
    else:
        dots_1 = paper[:, :fold_coord].astype(bool)
        dots_2 = paper[:, fold_coord + 1:].astype(bool)
        paper = dots_1 + np.fliplr(dots_2)
    return np.sum(paper)

def get_code(file):
    inputs = np.char.strip(np.array(open(file, 'r').readlines()))
    blank = np.nonzero(inputs == '')[0][0]
    dots = inputs[:blank]
    instructions = inputs[blank + 1:]
    rows = []
    cols = []
    for dot in dots:
        col, row = dot.split(',')
        cols.append(col)
        rows.append(row)
    rows = np.array(rows, dtype = int)
    cols = np.array(cols, dtype = int)
    row_size = np.max(rows)
    col_size = np.max(cols)
    paper = np.zeros((row_size + 1, col_size + 1))
    paper[(rows, cols)] = 1
    for fold in instructions:
        fold_xy, fold_coord = fold.split()[2].split('=')
        fold_coord = int(fold_coord)
        if fold_xy == 'y':
            dots_1 = paper[:fold_coord, :].astype(bool)
            dots_2 = paper[fold_coord + 1:].astype(bool)
            paper = dots_1 + np.flipud(dots_2)
        else:
            dots_1 = paper[:, :fold_coord].astype(bool)
            dots_2 = paper[:, fold_coord + 1:].astype(bool)
            paper = dots_1 + np.fliplr(dots_2)
    np.set_printoptions(linewidth=400)
    paper = paper.astype(int).astype(str)
    paper[paper == '0'] = '-'
    paper[paper == '1'] = '#'
    print(paper)

print(fold_once('input.txt'))
get_code('input.txt')

