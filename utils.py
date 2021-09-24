from typing import List
from random import shuffle

Grid = List[List[int]]


def display(grid: Grid) -> None:
    for row in grid:
        print(row)
    return


def random_list() -> List[int]:
    lst = list(range(1, 10))
    shuffle(lst)
    return lst
