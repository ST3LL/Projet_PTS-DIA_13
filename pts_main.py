import time
from copy import deepcopy
import random
from typing import List, Dict
import pickle

from sudoku_base import Sudoku
from sudoku_case_to_case import SudokuCaseToCase
from sudoku_case_to_group import SudokuCaseToGroup
from sudoku_faisceau import SudokuFaisceau
from sudoku_mrv import SudokuMRV
from sudoku_vanilla import SudokuVanilla
from utils import Region_map, build_vanilla_region_map

D_SUDOKU_BY_NAME = {
    'vanilla': SudokuVanilla,
    'case to case': SudokuCaseToCase,
    'case to group': SudokuCaseToGroup,
    'mrv': SudokuMRV,
    'faisceau': SudokuFaisceau
}


def get_models_and_rules() -> Dict[str, List[str]]:
    return {
        model_name: list(filter(lambda x: x.startswith('rule_'), dir(model)))
        for model_name, model in D_SUDOKU_BY_NAME.items()
    }


def build_sudoku(model_name: str, region_map: Region_map, ruleset_name: List[str]) -> Sudoku:
    model_class = D_SUDOKU_BY_NAME[model_name]
    ruleset = {getattr(model_class, rule_name) for rule_name in ruleset_name}
    sudoku_model = model_class(region_map, ruleset)
    sudoku_model.solve_mrv(save=True)
    print(sudoku_model)
    print(sudoku_model.solve_time)
    sudoku_model.thin_random()
    print(sudoku_model)
    return sudoku_model


if __name__ == '__main__':
    build_sudoku('mrv', build_vanilla_region_map(5), ['rule_vanilla'])
