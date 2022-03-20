import time
from copy import deepcopy
from typing import Set, Optional, Tuple

from sudoku_mrv import SudokuMRV
from utils import Case, Region_map, Rule, EMPTY, Grid


class SudokuFaisceau(SudokuMRV):
    last_valid_grid: Optional[Grid]

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super().__init__(region_map, ruleset)
        self.last_valid_grid = None

    def solve(self, find: int = 1, save: bool = False) -> int:
        def solve_aux() -> None:
            case, is_correct = self.get_target()
            if self.last_valid_grid is None and not is_correct:
                self.last_valid_grid = deepcopy(self.grid)

            if case is None:
                return

            row, col = case
            self.place(row, col, min(self.conflicts[(row, col)].items(), key=lambda x: x[-1])[0])
            solve_aux()

        self.move_history.clear()
        solve_aux()
        if self.last_valid_grid is None:
            self.last_valid_grid = deepcopy(self.grid)

        if save:
            self.solution = deepcopy(self.grid)
        return 1

    def get_target(self) -> Tuple[Optional[Case], bool]:
        minimum = self.dim + 1
        min_case = None
        false_val = None

        for k, v in self.nb_moves.items():
            if self.grid[k[0]][k[1]] != EMPTY:
                continue
            if not v:
                false_val = k
            elif v < minimum:
                minimum = v
                min_case = k

        if minimum == self.dim + 1:
            return false_val, False
        return min_case, True
