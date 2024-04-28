from typing import Generator
from sortvis.abc import SortAlgoVis
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygame import Color


class Insertion(SortAlgoVis):
    def vis_steps(self) -> Generator[list[tuple[int, Color]], None, None]:
        ...
