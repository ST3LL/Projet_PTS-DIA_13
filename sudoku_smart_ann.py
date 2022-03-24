from copy import deepcopy
from math import sqrt
from typing import Dict, Set

import numpy as np
from keras.models import Model
from tensorflow.python.keras.utils.np_utils import to_categorical

from sudoku_base import Sudoku
from sudoku_quick_ann import SudokuQuickANN
from utils import load_models, Region_map, Rule


class SudokuSmartANN(SudokuQuickANN):
    threshold: float = 0.90

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super().__init__(region_map, ruleset)
    # def solve(self, find: int = 1, save: bool = False) -> int:
    #     # print("self.string_to_tensor(self.grid_to_string())", self.string_to_tensor(self.grid_to_string()))
    #     grids = self.string_to_tensor(self.grid_to_string()).argmax(3)
    #     solver = self.d_ann_by_dim[int(sqrt(self.dim))]
    #     for _ in range((grids == 0).sum((1, 2)).max()):
    #         preds = np.array(solver.predict(to_categorical(grids)))
    #         probs = preds.max(2).T
    #         values = preds.argmax(2).T + 1
    #         zeros = (grids == 0).reshape((grids.shape[0], self.dim**2))
    #
    #         for grid, prob, value, zero in zip(grids, probs, values, zeros):
    #             if any(zero):
    #                 where = np.where(zero)[0]
    #                 confidence_position = where[prob[zero].argmax()]
    #                 confidence_value = value[confidence_position]
    #                 grid.flat[confidence_position] = confidence_value
    #     grid = grids[0]
    #     for case in self.ALL_COORD:
    #         self.place(*case, grid[case[0]][case[1]])
    #     return 1

