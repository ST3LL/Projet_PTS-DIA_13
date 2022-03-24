import json
import pickle
import re
from copy import deepcopy
from os import listdir
from typing import List, Dict

from sudoku_quick_ann import SudokuQuickANN
from sudoku_smart_ann import SudokuSmartANN
from sudoku_base import Sudoku
from sudoku_case_to_case import SudokuCaseToCase
from sudoku_case_to_group import SudokuCaseToGroup
from sudoku_constraint import SudokuConstraint
from sudoku_crook import SudokuCrook
from sudoku_faisceau import SudokuFaisceau
from sudoku_hill_climbing import SudokuHillClimbing
from sudoku_linear_programming import SudokuLinear
from sudoku_mrv import SudokuMRV
from sudoku_stochastic import SudokuStochastic
from sudoku_vanilla import SudokuVanilla
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
    'linear': SudokuLinear,
    'smart ann': SudokuSmartANN,
    'quick ann': SudokuQuickANN
}


def get_models_and_rules() -> Dict[str, List[str]]:
    return {
        model_name: list(filter(lambda x: x.startswith('rule_'), dir(model)))
        for model_name, model in D_SUDOKU_BY_NAME.items()
    }


def build_sudoku(model_name: str, region_map: Region_map, ruleset_name: List[str], difficulty: int = 100) -> Sudoku:
    model_class = D_SUDOKU_BY_NAME[model_name]
    ruleset = {getattr(model_class, rule_name) for rule_name in ruleset_name}
    sudoku_model = model_class(region_map, ruleset)
    sudoku_model.solve(save=True)
    sudoku_model.thin_random(difficulty)
    other_model = deepcopy(sudoku_model)
    other_model.solve()
    sudoku_model.move_history = deepcopy(other_model.move_history)
    return sudoku_model


def build_pickles(model_name: str, ruleset_name: List[str], l_dim: List[int], l_dif: List[int], quantity: int,
                  variations: int, degree_variation: int) -> None:
    for dim in l_dim:
        for dif in l_dif:
            print(f"d {dim}, lvl {dif}:")
            dst = f'sudoku_pickles/{model_name.replace(" ", "_")}_{dim}_{dif}_{quantity}_{variations}.pickle'
            with open(dst, 'wb') as f:
                l_sudoku = [
                    (build_sudoku(
                        model_name,
                        build_vanilla_region_map(dim),
                        ruleset_name,
                        dif
                    ), print(f'\t{_}'))[0] for _ in range(quantity)
                ]
                l_res = []
                for sudoku in l_sudoku:
                    l_res.append((sudoku.grid, sudoku.solution))
                    for _ in range(variations):
                        sudoku_variation = sudoku.build_variation(degree_variation)
                        l_res.append((sudoku_variation.grid, sudoku_variation.solution))
                pickle.dump(l_res, f)


def benchmark(l_models, ruleset, l_src, log_file):
    for src in l_src:
        dim, dif, q, v = [int(x) for x in re.findall(r"\d+", src)]
        region_map = build_vanilla_region_map(dim)
        with open(src, 'rb') as f_src:
            l_grid = pickle.load(f_src)
        for model_name in l_models:
            print(f'd {dim}, lvl {dif}, {q}*{v} by {model_name}')
            model_class = D_SUDOKU_BY_NAME[model_name]
            l_batch = []
            for i, (grid, sol) in enumerate(l_grid):
                solve_time, prop_valid = model_class.solve_grid(
                        region_map,
                        {getattr(model_class, rule_name) for rule_name in ruleset},
                        grid,
                        solution=sol
                    )
                print(f'd {dim}, lvl {dif}, {q}*{v} by {model_name}\t{i + 1}:\t{solve_time}\t{prop_valid}')
                l_batch.append((solve_time, prop_valid))
            with open(f"{log_file}_{model_name.replace(' ', '-')}_{dim}_{dif}_{q}_{v}.pickle", 'wb') as f:
                pickle.dump(l_batch, f)


def main_benchmark():
    src = 'sudoku_pickles'
    for model in ['stochastic']:
        benchmark(
            [model],
            {'rule_vanilla'},
            sorted([f"{src}/{x}" for x in listdir(src) if x.startswith('mrv_3_10_')]),
            "log_pickle/new_pickle"
        )
    for model in ['stochastic']:
        benchmark(
            [model],
            {'rule_vanilla'},
            sorted([f"{src}/{x}" for x in listdir(src) if x.startswith('mrv_3_20')]),
            "log_pickle/new_pickle"
        )


def main_build_pickles():
    build_pickles('mrv', ['rule_vanilla'], [2], [10 * i for i in range(10, 11)], 1000, 20, 20)


def main_visualize(src):
    with open(src, 'rb') as f:
        print(json.dumps(pickle.load(f), indent=2))


def misc():
    ws = 'Workshop'
    sudoku = SudokuVanilla(build_vanilla_region_map(4), {getattr(SudokuVanilla, 'rule_vanilla')})
    for i, src in enumerate(sorted(listdir(ws))):
        print(src)
        l_sudoku_and_variations = []
        l_grid = pickle.load(open(ws + '/' + src, 'rb'))
        for j, grid in enumerate(l_grid):
            sudoku.grid = grid
            l_sudoku_and_variations.extend([sudoku.grid] +
                                           [sudoku.build_variation(20) for n in range(10)]
                                           )
        pickle.dump(l_sudoku_and_variations, open(f"sudoku_pickles/scrap_4_{40 + 20*i}_{len(l_grid)}_{10}.pickle", 'wb'))


def other():
    src = 'sudoku_pickles/mrv_3_90_100_10.pickle'
    with open(src, 'rb') as f:
        l_grid = pickle.load(f)
    for i, (grid, sol) in enumerate(l_grid[428:430]):
        print('-----------', i, '-----------')
        # print(*grid, sep='\n')
        # SudokuANN.solve_grid(build_vanilla_region_map(3), set(), grid, show=True, solution=sol)


if __name__ == '__main__':
    pass
    # misc()
    # other()
    # main_benchmark()
    # main_build_pickles()
    # main_visualize('log_pickle/small.pickle')
