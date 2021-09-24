from utils import Grid, random_list, display
from typing import Set
from random import shuffle

# <editor-fold desc="Solvers">
def solve_brute(grid: Grid, row=0, col=0) -> bool:
    if row == 9:
        return True
    n_row, n_col = row + (col == 8), (col + 1) % 9
    if grid[row][col]:
        return solve_brute(grid, n_row, n_col)
    l_move = list(get_possible_move(grid, row, col))
    shuffle(l_move)
    for move in l_move:
        grid[row][col] = move
        if solve_brute(grid, n_row, n_col):
            return True
    grid[row][col] = 0
    return False


# </editor-fold>

# <editor-fold desc="Grid generation">
def generate_diag() -> Grid:
    grid = [[0 for _ in range(9)] for _ in range(9)]
    l_square = [random_list() for _ in range(3)]
    for i, square in enumerate(l_square):
        for j, sub in enumerate([square[k:k + 3] for k in range(0, 9, 3)]):
            grid[i * 3 + j][i * 3:i * 3 + 3] = sub
    return grid


def generate_full_grid() -> Grid:
    grid = generate_diag()
    solve_brute(grid)
    return grid


# </editor-fold>

# <editor-fold desc="Main functions">
def get_possible_move(grid: Grid, row: int, col: int) -> Set[int]:
    s_placed = set(grid[row]) | \
               {r[col] for r in grid} | \
               {x for sub in grid[3 * (row // 3): 3 * (row // 3) + 3] for x in sub[3 * (col // 3): 3 * (col // 3) + 3]}
    return set(range(1, 10)) - s_placed


def check_grid(grid: Grid) -> bool:
    return all([
        all([x in row for row in grid for x in range(1, 10)]),
        all([x in [row[col] for row in grid for col in range(9)] for x in range(1, 10)]),
        all([x in [y for c in range(9) for sub in grid[3 * c // 3: 3 * c // 3 + 3] for y in
                   sub[3 * c // 3: 3 * c // 3 + 3]] for x in range(1, 10)])
    ])


# </editor-fold>


if __name__ == '__main__':
    grid = generate_full_grid()
    display(grid)
