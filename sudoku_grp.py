from random import shuffle
from copy import deepcopy, copy
from typing import List, Optional, Set, Callable, Tuple, Dict, FrozenSet
# from more_termcolor import colored
import time

# <editor-fold desc="Type hinting & Constants">
Move = int
Grid = List[List[Optional[Move]]]
Region_map = List[List[Optional[int]]]
Case = Tuple[int, int]
Group = FrozenSet[Case]
GroupID = int
Rule = Callable[['Game'], Set[Group]]

EMPTY = 0
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
    dim = s_k.pop()
    # assert dim <= 16
    return dim


def build_vanilla_region_map(dim: int = 3) -> Region_map:
    return [[i // dim * dim + j // dim for j in range(dim ** 2)] for i in range(dim ** 2)]


def build_vanilla_ruleset() -> Set[Rule]:
    return {Game.rule_vanilla}


def calc_moveset(dim: int) -> Set[Move]:
    # return set(string.hexdigits[1:dim + 1])
    return {i for i in range(1, dim+1)}


# </editor-fold>


class Game:
    grid: Grid
    solution: Grid
    region_map: Region_map
    ruleset: Set[Rule]
    dim: int
    moveset: Set[Move]

    groupdict: Dict[GroupID, Group]
    moveset_of_group: Dict[GroupID, Dict[Move, int]]
    groupset_of_case: Dict[Case, Set[GroupID]]

    # <editor-fold desc="Dunder methods">
    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        self.region_map = region_map if region_map is not None else build_vanilla_region_map()
        self.dim = calc_dim(self.region_map)
        self.grid = [[EMPTY if case is not None else None for case in row] for row in self.region_map]
        self.ALL_COORD = self.build_all_coord()
        self.moveset = calc_moveset(self.dim)
        self.ruleset = ruleset if ruleset is not None else build_vanilla_ruleset()
        self.moveset_of_group = {}
        self.groupdict = {}
        self.groupset_of_case = {case: set() for case in self.ALL_COORD}
        self.build_group_architecture()
        self.solve_brute()
        self.solution = deepcopy(self.grid)
        self.thin_random()

    def __str__(self):
        return '\n'.join([
            '  '.join([
                # colored(
                hex(self.grid[i][j] - 1)[2:].upper()  # ,
                # L_COLOR[self.region_map[i][j] % len(L_COLOR)] if self.region_map[i][j] is not None else 30
                # )
                if self.grid[i][j] is not EMPTY else '.'
                if self.grid[i][j] is not None else '#'
                for j in range(len(self.grid[i]))])
            for i in range(len(self.grid))
        ]) + f"\n{sum([case in self.moveset for row in self.grid for case in row])} / " \
             f"{sum([case is not None for row in self.grid for case in row])}"

    def get_grid(self):
        return deepcopy(self.grid)

    def get_solution(self):
        return deepcopy(self.grid)
    # </editor-fold>

    # <editor-fold desc="Main methods">

    def build_all_coord(self) -> List[Case]:
        return [(i, j) for i in range(len(self.region_map)) for j in range(len(self.region_map[i]))]

    def build_groupset(self) -> Set[Group]:
        return {group for rule in self.ruleset for group in rule(self)}

    def build_group_architecture(self) -> None:
        for i, group in enumerate(self.build_groupset()):
            self.groupdict[i] = group
            self.moveset_of_group[i] = {move: 0 for move in self.moveset}
            for case in group:
                self.groupset_of_case[case].add(i)

    def is_case(self, row: int, col: int) -> bool:
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[row])

    def calc_possible_moves(self, row: int, col: int) -> Set[Move]:
        moveset = copy(self.moveset)
        for group in self.groupset_of_case[(row, col)]:
            moveset &= {move for move, conflict in self.moveset_of_group[group].items() if not conflict}
        return moveset

    def place(self, row: int, col: int, move: Move) -> None:
        val = self.grid[row][col]
        self.grid[row][col] = move
        for group in self.groupset_of_case[(row, col)]:
            if val != EMPTY:
                self.moveset_of_group[group][val] -= 1
            if move != EMPTY:
                self.moveset_of_group[group][move] += 1

    # </editor-fold>

    # <editor-fold desc="Solvers and Thinners">
    def solve_brute(self, row: int = 0, col: int = 0) -> int:
        if row == len(self.grid):
            return True
        next_row, next_col = row + (col == (len(self.grid[row]) - 1)), (col + 1) % len(self.grid[row])
        if self.grid[row][col] != EMPTY:
            return self.solve_brute(next_row, next_col)
        l_move = list(self.calc_possible_moves(row, col))
        shuffle(l_move)
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
            if self.solve_brute(i, j):
                thin[i][j] = EMPTY
            self.grid = deepcopy(thin)

    # </editor-fold>

    # <editor-fold desc="Rules">
    def rule_vanilla(self) -> Set[Group]:
        height, width = len(self.grid), len(self.grid[0])
        groupset = set()
        for group in (
                frozenset((
                        (row, col + j) for j in range(self.dim) if self.grid[row][col + j] is not None
                )) for row in range(height) for col in range(width - self.dim + 1)
        ):
            if len(group) != self.dim:
                continue
            groupset.add(group)
            groupset.add(frozenset((j, i) for i, j in group))
        d_region = {}
        for i, j in self.ALL_COORD:
            region = self.region_map[i][j]
            if region in d_region:
                d_region[region].add((i, j))
            else:
                d_region[region] = {(i, j)}
        for group in d_region.values():
            groupset.add(frozenset(group))
        return groupset
    # </editor-fold>


if __name__ == '__main__':
    print(Game(build_vanilla_region_map()))
