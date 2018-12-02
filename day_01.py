from itertools import count
from typing import List, Set


def parse_changes(path: str) -> List[int]:
    with open(path) as file:
        return [int(line.strip()) for line in file]


def apply_changes(initial: int, changes: List[int]) -> int:
    return initial + sum(changes)


def repeated_cumsum(initial: int, changes: List[int]):
    cumsum = initial
    for _ in count():
        for change in changes:
            yield cumsum
            cumsum += change


def calibrate(initial: int, changes: List[int]):
    seen: Set[int] = set()
    for value in repeated_cumsum(initial, changes):
        if value in seen:
            return value
        else:
            seen.add(value)


assert apply_changes(0, [1, -2, +3, +1]) == 3
assert apply_changes(0, [1, 1, 1]) == 3
assert apply_changes(0, [1, 1, -2]) == 0
assert apply_changes(0, [-1, -2, -3]) == -6

assert calibrate(0, [1, -1]) == 0
assert calibrate(0, [1, -2, 3, 1, 1, -2]) == 2
assert calibrate(0, [3, 3, 4, -2, -4]) == 10
assert calibrate(0, [-6, 3, 8, 5, -6]) == 5
assert calibrate(0, [7, 7, -2, -7, -4]) == 14

changes = parse_changes('data/day_01.txt')
print('First 5 changes:', changes[:5])
print('Last 5 changes:', changes[-5:])
print('Part 1:', sum(changes))
print('Part 2:', calibrate(0, changes))
