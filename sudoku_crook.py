import time
from copy import deepcopy
from random import shuffle
from typing import Set, Tuple, Optional, Dict

from sudoku_case_to_group import SudokuCaseToGroup
from utils import EMPTY, Region_map, Rule, Case, Move


class SudokuCrook(SudokuCaseToGroup):

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super().__init__(region_map, ruleset)

    def solve(self, find: int = 1, save: bool = False) -> int:
        def solve_aux(find: int = 1) -> int:
            best_case, best_moves = None, [None] * (self.dim + 1)
            d_case_one_move = {}
            for case_set in self.groupdict.values():
                s_move = set()
                d_case_by_move = {move: set() for move in self.moveset}
                for case in case_set:
                    if self.grid[case[0]][case[1]] not in {EMPTY, None}:
                        assert self.grid[case[0]][case[1]] not in s_move
                        s_move.add(self.grid[case[0]][case[1]])
                        continue
                    l_move = self.calc_possible_moves(*case)
                    for move in l_move:
                        d_case_by_move[move].add(case)
                    if len(l_move) < len(best_moves):
                        best_case, best_moves = case, l_move
                for move, s_case in d_case_by_move.items():
                    if len(s_case) == 1:
                        case = s_case.pop()
                        d_case_one_move[case] = (d_case_one_move[case] if case in d_case_one_move else set()) | {move}
                    elif len(s_case) == 0:
                        if move not in s_move:
                            return False
            for case, s_move in d_case_one_move.items():
                if len(s_move) != 1:
                    return False
                if len(s_move) < len(best_moves):
                    best_case, best_moves = case, s_move
                    break

            if best_case is None:
                return True
            best_moves = list(best_moves)
            shuffle(best_moves)
            found = 0
            for move in best_moves:
                self.place(best_case[0], best_case[1], move)
                found += solve_aux(find - found)
                if found >= find:
                    return found
            self.place(best_case[0], best_case[1], EMPTY)
            return found

        t = time.time()
        res = solve_aux(find)
        if save:
            self.solution = deepcopy(self.grid)
            self.solve_time = time.time() - t
        return res
