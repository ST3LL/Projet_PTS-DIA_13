import json
import pickle
from typing import List, Dict

from sudoku_base import Sudoku
from sudoku_case_to_case import SudokuCaseToCase
from sudoku_case_to_group import SudokuCaseToGroup
from sudoku_constraint import SudokuConstraint
from sudoku_crook import SudokuCrook
from sudoku_faisceau import SudokuFaisceau
from sudoku_hill_climbing import SudokuHillClimbing
from sudoku_mrv import SudokuMRV
from sudoku_vanilla import SudokuVanilla
from sudoku_stochastic import SudokuStochastic
from utils import Region_map, build_vanilla_region_map

D_SUDOKU_BY_NAME = {
    'vanilla': SudokuVanilla,
    'case to case': SudokuCaseToCase,
    'case to group': SudokuCaseToGroup,
    'mrv': SudokuMRV,
    'faisceau': SudokuFaisceau,
    'stochastic': SudokuStochastic,
    'constraint': SudokuConstraint,
    'crook': SudokuCrook,
    'hill climbing': SudokuHillClimbing,
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
    sudoku_model.solve(save=True)
    print(sudoku_model)
    sudoku_model.thin_random()
    print(sudoku_model)
    return sudoku_model


def benchmark(l_models, l_grid_and_region):
    ruleset = {'rule_vanilla'}
    d_log = {}
    for model_name in l_models:
        d_log[model_name] = []
        model_class = D_SUDOKU_BY_NAME[model_name]
        for i, (grid, region_map) in enumerate(l_grid_and_region):
            solve_time = model_class.solve_grid(
                region_map,
                {getattr(model_class, rule_name) for rule_name in ruleset},
                grid
            )
            d_log[model_name].append(solve_time)
            print(model_name, i, solve_time)
    with open('log.json', 'w') as f:
        json.dump(d_log, f)


if __name__ == '__main__':
    l_sudoku_pickle = [sudoku.grid for sudoku in pickle.load(open("l_sudoku_pickle.pickle", "rb"))][2:3]
    print(*l_sudoku_pickle[0], sep='\n')
    benchmark(['hill climbing'], [(grid, build_vanilla_region_map(3)) for grid in l_sudoku_pickle])
    # build_sudoku('stochastic', build_vanilla_region_map(2), ['rule_vanilla'])
