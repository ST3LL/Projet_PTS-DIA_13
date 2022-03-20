from random import shuffle
from typing import List, Optional, Tuple, FrozenSet, Callable, Set

# <editor-fold desc="Type hinting & Constants">
Move = int
Grid = List[List[Optional[Move]]]
Region_map = List[List[Optional[int]]]
Case = Tuple[int, int]
Group = FrozenSet[Case]
GroupID = int
Rule = Callable

EMPTY = 0
L_COLOR = [29, 30, 31, 32, 33, 34, 35, 36, 37]
L_COLOR_API = ['#ffc0cb', '#ffe4e1', '#008080', '#e6e6fa', '#ffd700', '#ffa500', '#ff7373', '#40e0d0', '#d3ffce',
               '#f0f8ff', '#c6e2ff', '#b0e0e6', '#faebd7', '#bada55', '#ffb6c1', '#fa8072', '#7fffd4', '#c39797',
               '#f08080', '#fff68f', '#20b2aa', '#ffc3a0', '#ff6666', '#ffdab9', '#c0d6e4', '#b4eeb4', '#cbbeb5',
               '#6897bb', '#a0db8e']


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


def get_color_list() -> List[str]:
    shuffle(L_COLOR_API)
    return L_COLOR_API


# </editor-fold>
