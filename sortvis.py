from pygame import Color
from random import shuffle
from typing import Generator

'''
All credit to GeeksForGeeks for their implementations
of the algorithms below, which I merely modified for
my purposes
'''

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


# Begin Merge Sort
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


# Begin Quick Sort
def partition(vals: int, low: int, high: int, r_val: int) -> VisSteps:
    pivot = vals[high]
    i = low - 1
    for j in range(low, high):
        if vals[j] < pivot:
            i += 1
            vals[i], vals[j] = vals[j], vals[i]
            yield quick_vis_helper(vals, pivot, j)
    vals[i + 1], vals[high] = vals[high], vals[i + 1]
    r_val[0] = i + 1


def quick(vals: list[int]) -> VisSteps:
    stack = []
    low = 0
    high = len(vals) - 1
    stack.append((low, high))
    while stack:
        low, high = stack.pop()
        if low < high:
            pi = [0]
            yield from partition(vals, low, high, pi)
            pi = pi[0]
            if pi - 1 > low:
                stack.append((low, pi - 1))
            if pi + 1 < high:
                stack.append((pi + 1, high))


def quick_vis_helper(vals: list[int],
                     pivot: int = -1,
                     selected: int = -1) -> list[tuple[int, Color]]:

    yielded = [(val, UNSORTED) if idx != pivot
               else (val, MARKED)
               for idx, val in enumerate(vals)]

    yielded = [val if idx != selected
               else (val[0], SELECTED)
               for idx, val in enumerate(yielded)]

    return yielded


# Begin Heap Sort
__sorted = 101


def heapify(vals: list[int], length: int, i: int) -> VisSteps:
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < length and vals[largest] < vals[left]:
        largest = left
    yield heap_vis_helper(vals, largest, left)

    if right < length and vals[largest] < vals[right]:
        largest = right
    yield heap_vis_helper(vals, largest, right)

    if largest != i:
        vals[i], vals[largest] = vals[largest], vals[i]
        yield heap_vis_helper(vals, largest, i)

        yield from heapify(vals, length, largest)


def heap(vals: list[int]) -> VisSteps:
    global __sorted
    __sorted = 101
    length = len(vals)

    for i in range(length // 2 - 1, -1, -1):
        yield from heapify(vals, length, i)

    for i in range(length - 1, 0, -1):
        vals[i], vals[0] = vals[0], vals[i]
        __sorted = i

        yield heap_vis_helper(vals, 0, i)

        yield from heapify(vals, i, 0)


def heap_vis_helper(vals: list[int],
                    root: int = -1,
                    selected: int = -1) -> list[tuple[int, Color]]:

    yielded = [(val, UNSORTED) if idx != root
               else (val, MARKED)
               for idx, val in enumerate(vals)]

    yielded = [val if idx != selected
               else (val[0], SELECTED)
               for idx, val in enumerate(yielded)]

    yielded = [val if idx < __sorted
               else (val[0], SORTED)
               for idx, val in enumerate(yielded)]

    return yielded


def count(vals: list[int], exp: int) -> VisSteps:
    n = len(vals)

    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = vals[i] // exp
        count[index % 10] += 1

        yielded = [(val, UNSORTED) if idx != i
                   else (val, SELECTED)
                   for idx, val in enumerate(vals)]
        yield yielded

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = vals[i] // exp
        output[count[index % 10] - 1] = vals[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        vals[i] = output[i]
        yield [(val, SORTED) if idx <= i
               else (val, UNSORTED)
               for idx, val in enumerate(vals)]


def radix(vals: list[int]) -> VisSteps:
    max_num = max(vals)

    exp = 1
    while max_num / exp >= 1:
        yield from count(vals, exp)
        exp *= 10
