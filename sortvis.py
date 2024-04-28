from pygame import Color
from random import shuffle
from typing import Generator

MARKED = Color(229, 242, 13)
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


def selection(vals: list[str]) -> VisSteps:
    for i in range(99):
        min_index = i
        for j in range(i + 1, 100):
            if vals[min_index] > vals[j]:
                min_index = j

            yielded = [(val, UNSORTED) if idx > i - 1
                       else (val, SORTED)
                       for idx, val in enumerate(vals)]

            yielded = [val if idx != j
                       else (val[0], SELECTED)
                       for idx, val in enumerate(yielded)]

            yielded = [val if idx != min_index
                       else (val[0], MARKED)
                       for idx, val in enumerate(yielded)]

            yield yielded

        vals[i], vals[min_index] = vals[min_index], vals[i]


def merge(vals: list[int]) -> VisSteps:
    current_size = 1
    while current_size < len(vals) - 1:
        left = 0
        while left < len(vals) - 1:
            mid = min(left + current_size - 1, len(vals) - 1)
            right = min(left + 2 * current_size - 1, len(vals) - 1)
            yield from combine(vals, left, mid, right)
            left += 2 * current_size
        current_size *= 2


def combine(vals: list[int], left: int, mid: int, right: int) -> VisSteps:
    n1 = mid - left + 1
    n2 = right - mid

    temp_left = [0] * n1
    temp_right = [0] * n2

    for i in range(0, n1):
        temp_left[i] = vals[left + i]

    for i in range(0, n2):
        temp_right[i] = vals[mid + 1 + i]

    i = 0
    j = 0
    k = left
    while i < n1 and j < n2:
        if temp_left[i] <= temp_right[j]:
            vals[k] = temp_left[i]
            i += 1
        else:
            vals[k] = temp_right[j]
            j += 1
        yield merge_vis_helper(vals, k)
        k += 1

    while i < n1:
        vals[k] = temp_left[i]
        i += 1
        yield merge_vis_helper(vals, k)
        k += 1

    while j < n2:
        vals[k] = temp_right[j]
        j += 1
        yield merge_vis_helper(vals, k)
        k += 1


def merge_vis_helper(vals: list[int],
                     selected: int) -> list[tuple[int, Color]]:

    yielded = [(val, UNSORTED) if idx != selected
               else (val, SELECTED)
               for idx, val in enumerate(vals)]

    return yielded


def bogo(vals: list[int]) -> VisSteps:
    while vals != sorted(vals):
        shuffle(vals)

        yield [(val, UNSORTED) for val in vals]


__all__ = ['insertion', 'bubble', 'selection', 'merge', 'bogo']
