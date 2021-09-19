from typing import Iterable, Mapping, Union
from tabulate import tabulate as tt


def tabulate(data: Union[Mapping[str, Iterable], Iterable[Iterable]]) -> str:
    return tt(data, headers='keys', tablefmt='fancy_grid')
