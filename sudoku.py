from typing import List, Set
from random import shuffle

Grid = List[List[int]]


def display(grid: Grid) -> None:
    for row in grid:
        print(row)
    return


def random_list() -> List[int]:
    lst = list(range(1, 10))
    shuffle(lst)
    return lst


def get_possible_move(grid: Grid, row: int, col: int) -> Set[int]:
    s_placed = set(grid[row]) | \
               {r[col] for r in grid} | \
               {x for sub in grid[3 * (row // 3): 3 * (row // 3) + 3] for x in sub[3 * (col // 3): 3 * (col // 3) + 3]}
    return set(range(1, 10)) - s_placed


def generate_diag() -> Grid:
    grid = [[0 for _ in range(9)] for _ in range(9)]
    l_case = [random_list() for _ in range(3)]
    for i, case in enumerate(l_case):
        for j, row in enumerate([case[k:k + 3] for k in range(0, 9, 3)]):
            grid[i * 3 + j][i * 3:i * 3 + 3] = row
    return grid


def solve_brute(grid: Grid, i=0, j=0) -> bool:
    if i == 9:
        return True
    n_i, n_j = i + (j == 8), (j + 1) % 9
    if grid[i][j]:
        return solve_brute(grid, n_i, n_j)
    l_move = list(get_possible_move(grid, i, j))
    shuffle(l_move)
    for move in l_move:
        grid[i][j] = move
        if solve_brute(grid, n_i, n_j):
            return True
    grid[i][j] = 0
    return False


def generate_full_grid() -> Grid:
    grid = generate_diag()
    solve_brute(grid)
    return grid


def check_grid(grid: Grid) -> bool:
    return all([
        all([x in row for row in grid for x in range(1, 10)]),
        all([x in [row[col] for row in grid for col in range(9)] for x in range(1, 10)]),
        all([x in [y for c in range(9) for sub in grid[3 * c // 3: 3 * c // 3 + 3] for y in
                   sub[3 * c // 3: 3 * c // 3 + 3]] for x in range(1, 10)])
    ])


if __name__ == '__main__':
    grid = generate_full_grid()
    display(grid)
    print(grid)
