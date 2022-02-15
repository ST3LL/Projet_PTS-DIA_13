import time
from random import shuffle
from copy import deepcopy
from typing import Dict, Set

from sudoku_case_to_group import SudokuCaseToGroup
from utils import Move, Case, Region_map, Rule, EMPTY


class SudokuMRV(SudokuCaseToGroup):
    nb_moves: Dict[Case, int]

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super().__init__(region_map, ruleset)
        self.nb_moves = {case: self.dim for case in self.ALL_COORD}

    def solve_mrv(self, find: int = 1, save: bool = False) -> int:
        def solve_mrv_aux(find: int = 1, placed: int = 0) -> int:
            if self.verif_full_grid(placed):
                return True
            case = self.min_move()
            if not case:
                return False
            row, col = case[0], case[1]
            l_move = list(self.calc_possible_moves(row, col))
            shuffle(l_move)
            found = 0
            for move in l_move:
                self.place(row, col, move)
                print(self)
                print(self.nb_moves)
                found += solve_mrv_aux(find-found, placed+1)
                if found >= find:
                    return found
            self.place(row, col, EMPTY)
            return found

        t = time.time()
        res = solve_mrv_aux(find, 0)
        if save:
            self.solution = deepcopy(self.grid)
            self.solve_time = time.time() - t
        return res

    def place(self, row: int, col: int, move: Move) -> None:
        val = self.grid[row][col]
        self.grid[row][col] = move
        cases = set()
        for group in self.groupset_of_case[(row, col)]:
            if val != EMPTY:
                self.moveset_of_group[group][val] -= 1
            if move != EMPTY:
                self.moveset_of_group[group][move] += 1

            for case in self.groupdict[group]:
                cases.add(case)

        for case in cases:
            self.calc_nb_moves(case)

    def calc_nb_moves(self, case: Case) -> None:
        self.nb_moves[case] = len(self.calc_possible_moves(case[0], case[1]))

    def min_move(self) -> Case:
        minimum = self.dim + 1
        min_case = None
        for k, v in self.nb_moves.items():
            if self.grid[k[0]][k[1]] != EMPTY:  # TODO EMPTY ou EMPTY & null ??
                continue
            if not v:
                min_case = None
                break
            if v < minimum:
                minimum = v
                min_case = k

        return min_case

    def verif_full_grid(self, placed: int) -> bool:
        return placed == self.dim * self.dim
