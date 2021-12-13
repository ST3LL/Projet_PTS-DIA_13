from copy import copy, deepcopy
from random import shuffle
from typing import List, Optional, Set, Callable, Tuple, FrozenSet, Dict

# <editor-fold desc="Type hinting & Constants">
Move = int
Grid = List[List[Optional[Move]]]
Region_map = List[List[Optional[int]]]
Case = Tuple[int, int]
Group = FrozenSet[Case]
GroupID = int
Rule = Callable

EMPTY = 0
L_COLOR = [29, 30, 31, 32, 33, 34, 35, 36, 37]


# </editor-fold>

# <editor-fold desc="help functions for the API">
def get_models():
    return list(D_SUDOKU_BY_NAME.keys())


def get_rules_of_model(model_name: str):
    return filter(lambda x: x.startswith('rule_'), dir(D_SUDOKU_BY_NAME[model_name]))


# </editor-fold>


# <editor-fold desc="help functions for Sudoku.__init__">
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
    raise NotImplementedError


def calc_moveset(dim: int) -> Set[Move]:
    return {i for i in range(1, dim + 1)}


# </editor-fold>

class Sudoku:
    grid: Grid
    solution: Grid
    region_map: Region_map
    ruleset: Set[Rule]
    dim: int
    moveset: Set[Move]

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        self.region_map = region_map if region_map is not None else build_vanilla_region_map()
        self.dim = calc_dim(self.region_map)
        self.moveset = calc_moveset(self.dim)
        self.ruleset = ruleset if ruleset is not None else build_vanilla_ruleset()
        self.grid = [[EMPTY if case is not None else None for case in row] for row in self.region_map]

    def __str__(self):
        return '\n'.join([
            '  '.join([
                hex(self.grid[i][j] - 1)[2:].upper()
                if self.grid[i][j] is not EMPTY else '.'
                if self.grid[i][j] is not None else '#'
                for j in range(len(self.grid[i]))])
            for i in range(len(self.grid))
        ]) + f"\n{sum([case in self.moveset for row in self.grid for case in row])} / " \
             f"{sum([case is not None for row in self.grid for case in row])}"

    def is_case(self, row: int, col: int) -> bool:
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[row])

    def place(self, row: int, col: int, move: Move) -> None:
        self.grid[row][col] = move

    def calc_possible_moves(self, row: int, col: int) -> Set[Move]:
        moveset = set(self.moveset)
        for rule in self.ruleset:
            moveset &= rule(self, row, col)
        return moveset

    def solve_brute(self, find: int = 1, save: bool = False):
        def solve_brute_aux(row: int = 0, col: int = 0, find: int = 1) -> int:
            if row == len(self.grid):
                return True
            next_row, next_col = row + (col == (len(self.grid[row]) - 1)), (col + 1) % len(self.grid[row])
            if self.grid[row][col] != EMPTY:
                return solve_brute_aux(next_row, next_col, find)
            l_move = list(self.calc_possible_moves(row, col))
            shuffle(l_move)
            found = 0
            for move in l_move:
                self.place(row, col, move)
                found += solve_brute_aux(next_row, next_col, find)
                if found >= find:
                    return found
            self.place(row, col, EMPTY)
            return found

        solve_brute_aux(0, 0, find)
        if save:
            self.solution = deepcopy(self.grid)

    def thin_random(self):
        case_order = [(i, j) for i in range(len(self.grid)) for j in range(len(self.grid[i]))]
        shuffle(case_order)
        thin = deepcopy(self.grid)
        for i, j in case_order:
            self.place(i, j, EMPTY)
            if self.solve_brute(find=2) == 1:
                thin[i][j] = EMPTY
            self.grid = deepcopy(thin)


class SudokuVanilla(Sudoku):
    def rule_vanilla(self, row: int, col: int) -> Set[Move]:
        return self.moveset & self.rule_row(row, col) & self.rule_col(row, col) & self.rule_region(row, col)

    def rule_row(self, row: int, col: int) -> Set[Move]:
        return self.moveset - {
            self.grid[row][j] for j in range(col - self.dim + 1, col + self.dim)
            if self.is_case(row, j)
        }

    def rule_col(self, row: int, col: int) -> Set[Move]:
        return self.moveset - {
            self.grid[i][col] for i in range(row - self.dim + 1, row + self.dim)
            if self.is_case(i, col)
        }

    def rule_region(self, row: int, col: int) -> Set[Move]:
        region = self.region_map[row][col]
        return self.moveset - {
            self.grid[i][j] for i in range(len(self.grid)) for j in range(len(self.grid[i]))
            if self.region_map[i][j] == region
        }

    def rule_king(self, row: int, col: int) -> Set[Move]:
        return self.moveset - {
            self.grid[i][j] for i in range(row - 1, row + 2) for j in range(col - 1, col + 2)
            if self.is_case(i, j)
        }

    def rule_knight(self, row: int, col: int) -> Set[Move]:
        base, mul = (1, 2), (1, -1)
        return self.moveset - {
            self.grid[row + i][col + j]
            for i, j in [(i * x, j * y) for i in base for j in base for x in mul for y in mul if i != j]
            if self.is_case(row + i, col + j)
        }


class SudokuCaseToCase(Sudoku):
    dependencies: Dict[Case, Set[Case]]
    conflicts: Dict[Case, Dict[Move, int]]

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super().__init__(region_map, ruleset)
        self.dependencies = self.build_dependencies()
        self.conflicts = self.build_conflicts()

    def build_dependencies(self) -> Dict[Case, Set[Case]]:
        return {
            (i, j): {case for rule in self.ruleset for case in rule(self, i, j)}
            for i in range(len(self.grid)) for j in range(len(self.grid[i]))
        }

    def build_conflicts(self) -> Dict[Case, Dict[Move, int]]:
        return {
            (i, j): {move: 0 for move in self.moveset}
            for i in range(len(self.grid)) for j in range(len(self.grid[i]))
        }

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

    def calc_possible_moves(self, row: int, col: int) -> Set[Move]:
        return {move for move, conflict in self.conflicts[(row, col)].items() if not conflict}

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


class SudokuCaseToGroup(Sudoku):
    groupdict: Dict[GroupID, Group]
    moveset_of_group: Dict[GroupID, Dict[Move, int]]
    groupset_of_case: Dict[Case, Set[GroupID]]

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super(Sudoku, self).__init__(region_map, ruleset)
        self.ALL_COORD = self.build_all_coord()
        self.moveset_of_group = {}
        self.groupdict = {}
        self.groupset_of_case = {case: set() for case in self.ALL_COORD}
        self.build_group_architecture()

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

    def rule_vanilla(self, **kwargs) -> Set[Group]:
        assert not kwargs
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


D_SUDOKU_BY_NAME = {
    'vanilla': SudokuVanilla,
    'case to case': SudokuCaseToCase,
    'case to group': SudokuCaseToGroup
}


def build_sudoku(model_name: str, region_map: Region_map, ruleset_name: List[str]) -> Sudoku:
    model_class = D_SUDOKU_BY_NAME[model_name]
    ruleset = {getattr(model_class, rule_name) for rule_name in ruleset_name}

    sudoku_model = model_class(region_map, ruleset)
    sudoku_model.solve_brute()
    return sudoku_model


if __name__ == '__main__':
    build_sudoku('vanilla', build_vanilla_region_map(), ['rule_row', 'rule_col', 'rule_region'])
