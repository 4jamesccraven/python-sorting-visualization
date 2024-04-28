from typing import Generator
from sortvis.abc import SortAlgoVis
from pygame import Color

SELECTED = Color((15, 233, 0))
SORTED = Color(255, 255, 255)
UNSORTED = Color(0, 0, 0)


class Insertion(SortAlgoVis):
    def vis_steps(self) -> Generator[list[tuple[int, Color]], None, None]:
        for i in range(1, 100):
            selected = self.vals[i]
            j = i - 1
            while j >= 0 and selected < self.vals[j]:
                self.vals[j + 1] = self.vals[j]
                j -= 1

                yielded = [(val, SORTED) if idx != j else (selected, SELECTED)
                           for idx, val in enumerate(self.vals)]

                yielded = [val if idx <= i else (val[0], UNSORTED)
                           for idx, val in enumerate(yielded)]

                yield yielded
            self.vals[j + 1] = selected
