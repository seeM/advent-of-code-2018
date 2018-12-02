from itertools import accumulate, chain, cycle
from typing import Iterable, Set, Optional


def parse_line(line: str) -> int:
    return int(str.strip(line))


def parse_changes(path: str) -> Iterable[int]:
    with open(path) as file:
        return map(parse_line, file.readlines())


def prepend(value: int, iterator: Iterable[int]) -> Iterable[int]:
    return chain([value], iterator)


def accumulate_changes(initial: int, changes: Iterable[int]) -> Iterable[int]:
    cycled = cycle(changes)
    prepended = prepend(initial, cycled)
    return accumulate(prepended)


def first_duplicate(iterator: Iterable[int]) -> Optional[int]:
    seen: Set[int] = set()
    for value in iterator:
        if value in seen:
            return value
        else:
            seen.add(value)
    else:
        return None


def calibrate(initial: int, changes: Iterable[int]) -> Optional[int]:
    return first_duplicate(accumulate_changes(initial, changes))


assert sum([1, -2, +3, +1]) == 3
assert sum([1, 1, 1]) == 3
assert sum([1, 1, -2]) == 0
assert sum([-1, -2, -3]) == -6

assert calibrate(0, [1, -1]) == 0
assert calibrate(0, [1, -2, 3, 1, 1, -2]) == 2
assert calibrate(0, [3, 3, 4, -2, -4]) == 10
assert calibrate(0, [-6, 3, 8, 5, -6]) == 5
assert calibrate(0, [7, 7, -2, -7, -4]) == 14

changes = list(parse_changes('data/day_01.txt'))
print('First 5 changes:', changes[:5])
print('Last 5 changes:', changes[-5:])
print('Part 1:', sum(changes))
print('Part 2:', calibrate(0, changes))
