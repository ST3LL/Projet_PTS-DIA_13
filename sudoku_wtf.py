from random import shuffle
from copy import deepcopy
from typing import List, Optional, Set, Callable, Tuple, Any, Dict
import string
from more_termcolor import colored
import time

# <editor-fold desc="Type hinting & Constants">
Move = str
Grid = List[List[Optional[Move]]]
Region_map = List[List[Optional[int]]]
Case = Tuple[int, int]
Rule = Callable[[Any, int, int], Set[Case]]

EMPTY = '0'
L_COLOR = [29, 30, 31, 32, 33, 34, 35, 36, 37]


# </editor-fold>

# <editor-fold desc="help functions for Game.__init__">
def calc_dim(region_map: Region_map) -> int:
    d_k = {}
    for row in region_map:
        for k in row:
            d_k[k] = d_k[k] + 1 if k in d_k else 1
    if None in d_k:
        del d_k[None]
    s_k = set(d_k.values())
    assert len(s_k) == 1
    return s_k.pop()


def build_vanilla_region_map(dim: int = 3) -> Region_map:
    return [[i // dim * dim + j // dim for j in range(dim ** 2)] for i in range(dim ** 2)]


def build_vanilla_ruleset() -> Set[Rule]:
    return {Game.rule_vanilla}


def calc_moveset(dim: int) -> Set[Move]:
    moves = string.digits[1:] + string.ascii_uppercase
    assert dim <= len(moves)
    return set(moves[:dim])


# </editor-fold>


class Game:
    grid: Grid
    region_map: Region_map
    ruleset: Set[Rule]
    dim: int
    moveset: Set[Move]
    dependencies: Dict[Case, Set[Case]]
    conflicts: Dict[Case, Dict[Move, int]]

    # <editor-fold desc="Dunder methods">
    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        self.region_map = region_map if region_map is not None else build_vanilla_region_map()
        self.dim = calc_dim(self.region_map)
        self.moveset = calc_moveset(self.dim)
        self.ruleset = ruleset if ruleset is not None else build_vanilla_ruleset()
        self.grid = [[EMPTY if case is not None else None for case in row] for row in self.region_map]
        self.dependencies = self.build_dependencies()
        self.conflicts = self.build_conflicts()
        self.solve_brute()
        # self.thin_random()

    def __str__(self):
        return '\n'.join([
            '  '.join([
                colored(
                    case,
                    L_COLOR[self.region_map[i][j] % len(L_COLOR)] if self.region_map[i][j] is not None else 30
                )
                if (case := self.grid[i][j]) is not None else '#'
                for j in range(len(self.grid[i]))])
            for i in range(len(self.grid))
        ]) + f"\n{sum([case in self.moveset for row in self.grid for case in row])} / " \
             f"{sum([case is not None for row in self.grid for case in row])}"

    # </editor-fold>

    # <editor-fold desc="Main methods">

    def build_dependencies(self) -> Dict[Case, Set[Case]]:
        return {
            (i, j): {case for rule in self.ruleset for case in rule(self, i, j)}
            for i in range(len(self.grid)) for j in range(len(self.grid[i]))
        }

    def build_conflicts(self) -> Dict[Case, Dict[Move, int]]:
        d = {
            (i, j): {move: 0 for move in self.moveset}
            for i in range(len(self.grid)) for j in range(len(self.grid[i]))
        }
        # for case in d:
        #     d[case][EMPTY] = inf
        return d

    def is_case(self, row: int, col: int) -> bool:
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[row])

    def calc_possible_moves(self, row: int, col: int) -> Set[Move]:
        return {move for move, conflict in self.conflicts[(row, col)].items() if not conflict}

    def place(self, row: int, col: int, move: Move) -> None:
        self.clean(row, col)
        self.do(row, col, move)

    def clean(self, row: int, col: int) -> None:
        if self.grid[row][col] != EMPTY:
            for case in self.dependencies[(row, col)]:
                self.conflicts[case][self.grid[row][col]] -= 1

    def do(self, row, col, move) -> None:
        self.grid[row][col] = move
        if move != EMPTY:
            for case in self.dependencies[(row, col)]:
                self.conflicts[case][move] += 1

    # </editor-fold>

    # <editor-fold desc="Solvers and Thinners">
    def solve_brute(self, row: int = 0, col: int = 0) -> int:
        if row == len(self.grid):
            return True
        next_row, next_col = row + (col == (len(self.grid[row]) - 1)), (col + 1) % len(self.grid[row])
        if self.grid[row][col] != EMPTY:
            return self.solve_brute(next_row, next_col)
        l_move = self.calc_possible_moves(row, col)
        for move in l_move:
            self.place(row, col, move)
            if self.solve_brute(next_row, next_col):
                return True
        self.place(row, col, EMPTY)
        return False

    def thin_random(self):
        case_order = [(i, j) for i in range(len(self.grid)) for j in range(len(self.grid[i]))]
        shuffle(case_order)
        thin = deepcopy(self.grid)
        for i, j in case_order:
            self.place(i, j, EMPTY)
            if self.solve_brute(i, j) == 1:
                thin[i][j] = EMPTY
            self.grid = deepcopy(thin)

    # </editor-fold>

    # <editor-fold desc="Rules">
    def rule_vanilla(self, row: int, col: int) -> Set[Case]:
        return self.rule_row(row, col) | self.rule_col(row, col) | self.rule_region(row, col)

    def rule_row(self, row: int, col: int) -> Set[Case]:
        return {
            (row, j) for j in range(max(0, col - self.dim + 1), min(col + self.dim, len(self.grid[row])))
        }

    def rule_col(self, row: int, col: int) -> Set[Case]:
        return {
            (i, col) for i in range(max(0, row - self.dim + 1), min(row + self.dim, len(self.grid)))
        }

    def rule_region(self, row: int, col: int) -> Set[Case]:
        region = self.region_map[row][col]
        return {
            (i, j) for i in range(len(self.grid)) for j in range(len(self.grid[i]))
            if self.region_map[i][j] == region
        }

    def rule_king(self, row: int, col: int) -> Set[Case]:
        ope = (-1, 1)
        return {
            (row + i, col + j) for i in ope for j in ope
            if self.is_case(i, j)
        }

    def rule_knight(self, row: int, col: int) -> Set[Case]:
        base, mul = (1, 2), (1, -1)
        return {
            (row + i, col + j)
            for i, j in [(i * x, j * y) for i in base for j in base for x in mul for y in mul if i != j]
            if self.is_case(row + i, col + j)
        }

    # </editor-fold>


if __name__ == '__main__':
    t = time.time()
    game = Game(build_vanilla_region_map(3))
    print(game)
    print(time.time() - t)
