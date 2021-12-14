from copy import copy
from typing import Dict, Set, List

from models import Sudoku
from utils import GroupID, Group, Move, Case, Region_map, Rule, EMPTY


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
