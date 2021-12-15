from copy import deepcopy
from typing import Dict, Set

from sudoku_base import Sudoku
from utils import Case, Move, Region_map, Rule, EMPTY


class SudokuCaseToCase(Sudoku):
    dependencies: Dict[Case, Set[Case]]
    conflicts: Dict[Case, Dict[Move, int]]

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super().__init__(region_map, ruleset)
        self.dependencies = self.build_dependencies()
        self.conflicts = self.build_conflicts()

    def build_dependencies(self) -> Dict[Case, Set[Case]]:
        return {
            (i, j): {case for rule in self.ruleset for case in rule(self, i, j)} - {(i, j)}
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
        ope = (-1, 0, 1)
        return {
            (row + i, col + j) for i in ope for j in ope
            if self.is_case(row + i, col + j)
        }

    def rule_knight(self, row: int, col: int) -> Set[Case]:
        base, mul = (1, 2), (1, -1)
        return {
            (row + i, col + j)
            for i, j in [(i * x, j * y) for i in base for j in base for x in mul for y in mul if i != j]
            if self.is_case(row + i, col + j)
        }

    def update_as(self, other_sudoku: 'SudokuCaseToCase'):
        super().update_as(other_sudoku)
        self.conflicts = deepcopy(other_sudoku.conflicts)
