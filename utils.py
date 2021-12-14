# <editor-fold desc="Type hinting & Constants">
from typing import List, Optional, Tuple, FrozenSet, Callable, Dict, Set

from sudoku_case_to_case import SudokuCaseToCase
from sudoku_case_to_group import SudokuCaseToGroup
from sudoku_vanilla import SudokuVanilla

Move = int
Grid = List[List[Optional[Move]]]
Region_map = List[List[Optional[int]]]
Case = Tuple[int, int]
Group = FrozenSet[Case]
GroupID = int
Rule = Callable

EMPTY = 0
L_COLOR = [29, 30, 31, 32, 33, 34, 35, 36, 37]

D_SUDOKU_BY_NAME = {
    'vanilla': SudokuVanilla,
    'case to case': SudokuCaseToCase,
    'case to group': SudokuCaseToGroup
}


# </editor-fold>

# <editor-fold desc="help functions for the API">
def get_models_and_rules() -> Dict[str, List[str]]:
    return {
        model_name: filter(lambda x: x.startswith('rule_'), dir(model))
        for model_name, model in D_SUDOKU_BY_NAME.items()
    }


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
