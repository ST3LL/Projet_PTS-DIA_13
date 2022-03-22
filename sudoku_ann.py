from copy import deepcopy
from math import sqrt
from typing import Dict, Set

import numpy as np
from keras.models import Model
from tensorflow.python.keras.utils.np_utils import to_categorical

from sudoku_base import Sudoku
from utils import load_models, Region_map, Rule


class SudokuANN(Sudoku):
    d_ann_by_dim: Dict[int, Model] = load_models()
    threshold: float = 0.90

    def __init__(self, region_map: Region_map = None, ruleset: Set[Rule] = None):
        super().__init__(region_map, ruleset)

    def solve(self, find: int = 1, save: bool = False) -> int:
        # print("self.grid_to_string()", self.grid_to_string())
        # print("self.string_to_tensor(self.grid_to_string())", self.string_to_tensor(self.grid_to_string()))
        grids = self.string_to_tensor(self.grid_to_string()).argmax(3)
        grid = grids[0]
        solver = self.d_ann_by_dim[int(sqrt(self.dim))]
        zeros = [(x, y) for x, y in zip(*np.where(grid == 0))]
        start_zeros = deepcopy(zeros)
        while zeros:
            pred = np.array(solver.predict(to_categorical(grids, num_classes=self.dim+1)))
            l_fill_pred = [pred[x*self.dim + y] for x, y in zeros]
            l_fill_val = [np.argmax(x) for x in l_fill_pred]
            l_fill_prob = [x.max() for x in l_fill_pred]
            stuck = True
            done = set()
            for i in range(len(zeros)):
                if l_fill_prob[i] >= self.threshold:
                    grid[zeros[i][0]][zeros[i][1]] = l_fill_val[i] + 1
                    done.add(i)
                    curr = zeros[i]
                    stuck = False
            if stuck:
                best = np.argmax(l_fill_prob)
                # print(stuck, sorted([round(x, 2) for x in l_fill_prob])[-3:])
                grid[zeros[best][0]][zeros[best][1]] = l_fill_val[best] + 1
                done.add(best)
            zeros = [zero for i, zero in enumerate(zeros) if i not in done]
        for case in start_zeros:
            self.place(*case, grid[case[0]][case[1]])
        return 1

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

