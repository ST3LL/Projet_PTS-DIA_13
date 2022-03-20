import time
from copy import deepcopy
from random import shuffle
from typing import Set

import pulp
from pulp import PULP_CBC_CMD

from sudoku_case_to_group import SudokuCaseToGroup
from utils import Region_map, Rule


class SudokuLinear(SudokuCaseToGroup):
    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super().__init__(region_map, ruleset)

    def solve(self, find: int = 1, save: bool = False) -> int:
        if find != 1:
            return find

        linear = pulp.LpProblem("SudokuLinear")
        linear.setObjective(pulp.lpSum(0))
        dims = list(range(self.dim))
        shuffle(dims)
        moves = list(self.moveset)
        shuffle(moves)
        grid = pulp.LpVariable.dicts("grid", (dims, dims, moves), cat='Binary')

        for row in dims:  # only one value per cell constraint
            for col in dims:
                linear.addConstraint(pulp.LpConstraint(e=pulp.lpSum([grid[row][col][value] for value in moves]),
                                                       sense=pulp.LpConstraintEQ, rhs=1))

        for rule in self.groupdict.values():  # rules constraints
            for move in moves:
                linear.addConstraint(pulp.LpConstraint(e=pulp.lpSum([grid[pos[0]][pos[1]][move]*move for pos in rule]),
                                                       sense=pulp.LpConstraintEQ, rhs=move))
        linear.solve(PULP_CBC_CMD(msg=False))

        for row in dims:
            for col in dims:
                for move in moves:
                    if pulp.value(grid[row][col][move]):
                        self.place(row, col, move)

        if save:
            self.solution = deepcopy(self.grid)
