from pygame import Color
from typing import Generator

SELECTED = Color(15, 233, 0)
SORTED = Color(255, 255, 255)
UNSORTED = Color(0, 0, 0)

VisSteps = Generator[list[tuple[int, Color]], None, None]


def insertion(vals: list[int]) -> VisSteps:
    for i in range(1, 100):
        selected = vals[i]
        j = i - 1
        while j >= 0 and selected < vals[j]:
            vals[j + 1] = vals[j]
            j -= 1

            yielded = [(val, SORTED) if idx != j else (selected, SELECTED)
                       for idx, val in enumerate(vals)]

            yielded = [val if idx <= i else (val[0], UNSORTED)
                       for idx, val in enumerate(yielded)]

            yield yielded
        vals[j + 1] = selected


def bubble(vals: list[int]) -> VisSteps:
    for i in range(100):
        swapped = False
        for j in range(99 - i):
            if vals[j] > vals[j + 1]:
                vals[j], vals[j + 1] = vals[j + 1], vals[j]
                swapped = True

                yielded = [(val, UNSORTED) if idx != j
                           else (val, SELECTED)
                           for idx, val in enumerate(vals)]

                yielded = [val if idx <= (99 - i)
                           else (val[0], SORTED)
                           for idx, val in enumerate(yielded)]

                yield yielded

        if not swapped:
            break


__all__ = ['insertion', 'bubble']
