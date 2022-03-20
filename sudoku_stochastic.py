from typing import Set, List, Dict
from math import sqrt
from random import shuffle

from sudoku_vanilla import SudokuVanilla
from utils import Region_map, Rule, Case, EMPTY


class SudokuStochastic(SudokuVanilla):
    l_frozen_case: List[Dict[int, Case]]

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super().__init__(region_map, ruleset)
        self.stride = self.calc_stride()
        self.l_frozen_case = self.build_frozen_case()
        
    def calc_stride(self):
        stride = sqrt(self.dim)
        if stride != int(stride):
            raise ValueError(f"Incorrect dimension for stochastic: {self.dim}")

        return int(stride)

    def build_frozen_case(self) -> List[Dict[int, Case]]:
        l_frozen_case = []

        for i_region in range(self.stride):
            for j_region in range(self.stride):
                d_frozen_case = {}

                for i_case in range(self.stride * i_region, self.stride * i_region + self.stride):
                    for j_case in range(self.stride * j_region, self.stride * j_region + self.stride):
                        if self.grid[i_case][j_case] != EMPTY:
                            d_frozen_case[self.grid[i_case][j_case]] = (i_case, j_case)

                l_frozen_case.append(d_frozen_case)

        return l_frozen_case

    def solve(self, find: int = 2, save: bool = False) -> int:
        def fill_grid() -> None:
            for region_id in range(self.dim):
                fill_region(region_id)

        def fill_region(region_id: int) -> None:
            d_frozen_case = self.l_frozen_case[region_id]
            l_moveset = list(self.moveset - set(d_frozen_case.keys()))
            shuffle(l_moveset)
            l_moveset = l_moveset.__iter__()
            i_region, j_region = region_id // self.stride, region_id % self.stride
            for i_case in range(self.stride * i_region, self.stride * i_region + self.stride):
                for j_case in range(self.stride * j_region, self.stride * j_region + self.stride):
                    if self.grid[i_case][j_case] in d_frozen_case:
                        continue
                    self.place(i_case, j_case, next(l_moveset))

        def solve_aux() -> None:
            def calc_region_conflicts() -> List[int]:
                l_conflicts = []

                for i_region in range(self.stride):
                    for j_region in range(self.stride):
                        n_conflicts = 0

                        for i_case in range(self.stride * i_region, self.stride * i_region + self.stride):
                            for j_case in range(self.stride * j_region, self.stride * j_region + self.stride):
                                if self.grid[i_case][j_case] in self.l_frozen_case[j_region]:
                                    continue
                                n_conflict_row, n_conflict_col = self.conflict_row(i_case, j_case), self.conflict_col(i_case, j_case)
                                n_conflicts += n_conflict_row + n_conflict_col

                        l_conflicts.append(n_conflicts)

                return l_conflicts

            while True:
                l_region_conflicts = calc_region_conflicts()
                if not any(l_region_conflicts):
                    break
                target = max(enumerate(l_region_conflicts), key=lambda x: x[-1])[0]
                fill_region(target)

        self.move_history.clear()
        fill_grid()
        solve_aux()

        return 1
