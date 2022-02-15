import time
from random import shuffle
from copy import deepcopy
from typing import Dict, Set, Optional

from sudoku_case_to_case import SudokuCaseToCase
from utils import Move, Case, Region_map, Rule, EMPTY


class SudokuMRV(SudokuCaseToCase):
    nb_moves: Dict[Case, int]

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super().__init__(region_map, ruleset)
        shuffle(self.ALL_COORD)
        self.nb_moves = {case: self.dim for case in set(self.ALL_COORD)}

    def solve_mrv(self, find: int = 1, save: bool = False) -> int:
        def solve_mrv_aux(find: int = 1, placed: int = 0) -> int:
            case = self.min_move()
            if not case:
                return case is not None

            row, col = case[0], case[1]
            l_move = list(self.calc_possible_moves(row, col))
            shuffle(l_move)
            found = 0
            for move in l_move:
                self.place(row, col, move)
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
        super().place(row, col, move)
        for case in self.dependencies[(row, col)]:
            self.calc_nb_moves(case)

    def calc_nb_moves(self, case: Case) -> None:
        self.nb_moves[case] = len(self.calc_possible_moves(case[0], case[1]))

    def min_move(self) -> [Optional[Case], bool]:
        minimum = self.dim + 1
        min_case = None
        for k, v in self.nb_moves.items():
            if self.grid[k[0]][k[1]] != EMPTY:
                continue
            if not v:
                return None
            if v < minimum:
                minimum = v
                min_case = k

        if min_case is None:
            return False

        return min_case
