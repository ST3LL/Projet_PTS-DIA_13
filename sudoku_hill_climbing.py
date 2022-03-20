from copy import deepcopy
from random import shuffle, sample
from typing import Set, Tuple, Generator

from sudoku_case_to_case import SudokuCaseToCase
from utils import Region_map, Rule, Case, EMPTY, peek


class SudokuHillClimbing(SudokuCaseToCase):
    s_free_case: Set[Case]

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super().__init__(region_map, ruleset)

    def solve(self, find: int = 1, save: bool = False) -> int:
        def solve_aux():
            self.fill_free_cases()
            current_conflicts = self.calc_conflicts()
            while True:
                stuck = True
                sons = peek(self.generate_sons())
                if sons is None:
                    return
                conflicts, a, b = min(sons, key=lambda x: x[0])
                if conflicts < current_conflicts:
                    self.switch_case(a, b)
                    current_conflicts = conflicts
                    stuck = False
                if not current_conflicts:
                    return
                if stuck:
                    # print('stuck at', current_conflicts)
                    self.random_restart()
                    current_conflicts = self.calc_conflicts()

        self.s_free_case = {case for case in self.ALL_COORD if self.grid[case[0]][case[1]] == EMPTY}
        solve_aux()
        if save:
            self.solution = deepcopy(self.grid)
        return 1

    def fill_free_cases(self) -> None:
        for i in range(len(self.grid)):
            l_moveset = list(self.moveset - {self.grid[i][j] for j in range(len(self.grid[i])) if (i, j) not in self.s_free_case})
            shuffle(l_moveset)
            for j in range(len(self.grid[i])):
                if (i, j) not in self.s_free_case:
                    continue
                self.place(i, j, l_moveset.pop())

    def generate_sons(self) -> Generator[Tuple[int, Case, Case], None, None]:
        l_free_case = list(self.s_free_case)
        shuffle(l_free_case)
        son = deepcopy(self)
        for i in range(len(self.grid)):
            for j1 in range(len(self.grid[i])):
                for j2 in range(len(self.grid[i])):
                    if j1 == j2 or (i, j1) not in self.s_free_case or (i, j2) not in self.s_free_case:
                        continue
                    son.switch_case((i, j1), (i, j2))
                    conflicts = son.calc_conflicts()
                    son.switch_case((i, j1), (i, j2))
                    yield conflicts, (i, j1), (i, j2)

    def switch_case(self, a: Case, b: Case) -> None:
        b_move = self.grid[b[0]][b[1]]
        self.place(b[0], b[1], self.grid[a[0]][a[1]])
        self.place(a[0], a[1], b_move)

    def random_restart(self) -> None:
        for i in range(len(self.grid)):
            l_free_case = [(i, j) for j in range(len(self.grid[i])) if (i, j) in self.s_free_case]
            if len(l_free_case) < 2:
                continue
            self.switch_case(*sample(l_free_case, 2))

