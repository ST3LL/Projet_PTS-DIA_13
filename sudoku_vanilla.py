from typing import Set

from sudoku_base import Sudoku
from utils import Move, Grid
from random import shuffle


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
