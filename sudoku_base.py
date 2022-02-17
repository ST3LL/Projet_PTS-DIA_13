import time
from copy import deepcopy
from math import sqrt
from random import shuffle, sample
from typing import Set, List

from utils import Grid, Region_map, Rule, Move, calc_dim, calc_moveset, EMPTY, Case


class Sudoku:
    grid: Grid
    solution: Grid
    region_map: Region_map
    ruleset: Set[Rule]
    dim: int
    moveset: Set[Move]
    solve_time: float

    def __init__(self, region_map: Region_map, ruleset: Set[Rule]):
        self.region_map = region_map
        self.ALL_COORD = self.build_all_coord()
        self.dim = calc_dim(self.region_map)
        self.moveset = calc_moveset(self.dim)
        self.ruleset = ruleset
        self.grid = [[EMPTY if case is not None else None for case in row] for row in self.region_map]

    def __str__(self):
        return '\n'.join([
            '  '.join([
                hex(self.grid[i][j])[2:].upper()
                if self.grid[i][j] is not EMPTY else '.'
                if self.grid[i][j] is not None else '#'
                for j in range(len(self.grid[i]))])
            for i in range(len(self.grid))
        ]) + f"\n{sum([case in self.moveset for row in self.grid for case in row])} / " \
             f"{sum([case is not None for row in self.grid for case in row])}"

    def is_case(self, row: int, col: int) -> bool:
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[row])

    def place(self, row: int, col: int, move: Move) -> None:
        self.grid[row][col] = move

    def calc_possible_moves(self, row: int, col: int) -> Set[Move]:
        moveset = set(self.moveset)
        for rule in self.ruleset:
            moveset &= rule(self, row, col)
        return moveset

    def solve_thin(self):
        return Sudoku.solve(self, find=2, save=True)

    def solve(self, find: int = 1, save: bool = False) -> int:
        def solve_aux(row: int = 0, col: int = 0, find: int = 1) -> int:
            if row == len(self.grid):
                return True
            next_row, next_col = row + (col == (len(self.grid[row]) - 1)), (col + 1) % len(self.grid[row])
            if self.grid[row][col] != EMPTY:
                return solve_aux(next_row, next_col, find)
            l_move = list(self.calc_possible_moves(row, col))
            shuffle(l_move)
            found = 0
            for move in l_move:
                self.place(row, col, move)
                found += solve_aux(next_row, next_col, find-found)
                if found >= find:
                    return found
            self.place(row, col, EMPTY)
            return found

        t = time.time()
        res = solve_aux(0, 0, find)
        if save:
            self.solution = deepcopy(self.grid)
            self.solve_time = time.time() - t
        return res

    def thin_random(self):
        case_order = [(i, j) for i in range(len(self.grid)) for j in range(len(self.grid[i]))]
        shuffle(case_order)
        thinned_sudoku = deepcopy(self)
        for i, j in case_order:
            self.place(i, j, EMPTY)
            if self.solve_thin() == 1:
                thinned_sudoku.place(i, j, EMPTY)
            self.update_as(thinned_sudoku)

    def build_all_coord(self) -> List[Case]:
        return [(i, j) for i in range(len(self.region_map)) for j in range(len(self.region_map[i]))]

    def update_as(self, other_sudoku: 'Sudoku'):
        self.grid = deepcopy(other_sudoku.grid)

    def variation_permutation(self) -> Grid:
        l_map = list(self.moveset)
        shuffle(l_map)
        d_map = {old_move: l_map[i] for i, old_move in enumerate(self.moveset)}
        return [
            [d_map[move] for move in row]
            for row in self.grid
        ]

    def variation_rotation(self) -> Grid:
        return [[self.grid[j-1][-i] for j in range(1, self.dim+1)] for i in range(1, self.dim+1)]

    def variation_shuffle_row(self) -> Grid:
        dim_reg = int(sqrt(self.dim))
        dim_gp = list(map(lambda x: x*dim_reg, range(dim_reg)))
        return [self.grid[i+j] for j in sample(dim_gp, len(dim_gp)) for i in sample(list(range(dim_reg)), dim_reg)]

    def variation_symmetry_horizontal(self) -> Grid:
        return self.grid[::-1]

    def variation_symmetry_diagonal(self) -> Grid:
        return [[self.grid[self.dim-j][self.dim-i]for j in range(1, self.dim+1)] for i in range(1, self.dim+1)]
