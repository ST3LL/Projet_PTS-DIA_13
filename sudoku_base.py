from copy import deepcopy
from random import shuffle
from typing import Set

from utils import Grid, Region_map, Rule, Move, calc_dim, calc_moveset, build_vanilla_region_map, \
    build_vanilla_ruleset, EMPTY


class Sudoku:
    grid: Grid
    solution: Grid
    region_map: Region_map
    ruleset: Set[Rule]
    dim: int
    moveset: Set[Move]

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        self.region_map = region_map if region_map is not None else build_vanilla_region_map()
        self.dim = calc_dim(self.region_map)
        self.moveset = calc_moveset(self.dim)
        self.ruleset = ruleset if ruleset is not None else build_vanilla_ruleset()
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

    def solve_brute(self, find: int = 1, save: bool = False) -> int:
        def solve_brute_aux(row: int = 0, col: int = 0, find: int = 1) -> int:
            if row == len(self.grid):
                return True
            next_row, next_col = row + (col == (len(self.grid[row]) - 1)), (col + 1) % len(self.grid[row])
            if self.grid[row][col] != EMPTY:
                return solve_brute_aux(next_row, next_col, find)
            l_move = list(self.calc_possible_moves(row, col))
            shuffle(l_move)
            found = 0
            for move in l_move:
                self.place(row, col, move)
                found += solve_brute_aux(next_row, next_col, find-found)
                if found >= find:
                    return found
            self.place(row, col, EMPTY)
            return found

        res = solve_brute_aux(0, 0, find)
        if save:
            self.solution = deepcopy(self.grid)
        return res

    def thin_random(self):
        case_order = [(i, j) for i in range(len(self.grid)) for j in range(len(self.grid[i]))]
        shuffle(case_order)
        thinned_sudoku = deepcopy(self)
        for i, j in case_order:
            self.place(i, j, EMPTY)
            if self.solve_brute(find=2) == 1:
                thinned_sudoku.place(i, j, EMPTY)
            self.update_as(thinned_sudoku)

    def update_as(self, other_sudoku: 'Sudoku'):
        self.grid = deepcopy(other_sudoku.grid)
