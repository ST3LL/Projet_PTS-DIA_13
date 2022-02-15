import time
from random import shuffle
from copy import deepcopy
from typing import Dict, Set, Optional, Tuple

from sudoku_case_to_case import SudokuCaseToCase
from sudoku_mrv import SudokuMRV
from utils import Move, Case, Region_map, Rule, EMPTY


class SudokuFaisceau(SudokuMRV):

    def min_move(self) -> Tuple[Optional[Case], bool]:
        minimum = self.dim + 1
        min_case = None
        is_correct = True
        for k, v in self.nb_moves.items():
            if v < 0:
                print('coucou')
            if self.grid[k[0]][k[1]] != EMPTY:
                continue
            if not v:
                is_correct = False
            elif v < minimum:
                minimum = v
                min_case = k

        return min_case, is_correct
