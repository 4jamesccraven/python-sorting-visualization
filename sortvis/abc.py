from abc import ABC, abstractmethod
from typing import Generator
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygame import Color


class SortAlgoVis(ABC):
    def __init__(self, vals: list[int]) -> None:
        '''Initialises the sorting algorithm visualiser
        with a list of 100 ints'''
        super().__init__()
        if len(vals) != 100 or not isinstance(vals, list):
            raise ValueError('Argument should be a list of ints with size 100')

    @abstractmethod
    def vis_steps(self) -> Generator[list[tuple[int, Color]], None, None]:
        '''yields the internal array in steps to visualise them'''
        ...
