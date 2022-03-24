import time
from copy import deepcopy
from random import shuffle
from typing import Set, Tuple, Optional, Dict

from sudoku_case_to_group import SudokuCaseToGroup
from utils import EMPTY, Region_map, Rule, Case, Move


class SudokuConstraint(SudokuCaseToGroup):
    nb_moves: Dict[Case, int]

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super().__init__(region_map, ruleset)
        shuffle(self.ALL_COORD)
        self.nb_moves = {case: self.dim for case in set(self.ALL_COORD)}

    def solve(self, find: int = 1, save: bool = False) -> int:
        def solve_aux(find: int = 1) -> int:
            case, is_correct = self.get_target()
            if case is None:
                return is_correct

            row, col = case[0], case[1]
            l_move = list(self.calc_possible_moves(row, col))
            shuffle(l_move)
            found = 0
            for move in l_move:
                self.place(row, col, move)
                found += solve_aux(find - found)
                if found >= find:
                    return found
            self.place(row, col, EMPTY)
            return found

        self.move_history.clear()
        res = solve_aux(find)
        if save:
            self.solution = deepcopy(self.grid)
        return res

    def get_target(self) -> Tuple[Optional[Case], bool]:
        minimum = self.dim + 1
        min_case = None
        for case in self.groupset_of_case:
            if self.grid[case[0]][case[1]] != EMPTY:
                continue
            v = self.nb_moves[case]
            if v < minimum:
                minimum = v
                min_case = case
        if not minimum:
            return None, False

        return min_case, True

    def place(self, row: int, col: int, move: Move) -> None:
        super().place(row, col, move)
        for group_id in self.groupset_of_case[(row, col)]:
            for case in self.groupdict[group_id]:
                if self.grid[case[0]][case[1]] == EMPTY:
                    self.calc_nb_moves(case)

    def calc_nb_moves(self, case):
        return len(self.calc_possible_moves(*case))
