from collections import Counter
from itertools import combinations
from functools import partial, reduce
from operator import add as add_, mul, ne
from typing import Iterable, List, Tuple, Optional


def parse_input(path: str) -> Iterable[str]:
    with open(path) as file:
        return [line.strip() for line in file]


def check(iterable: Iterable) -> Tuple[int, int]:
    counts = Counter(iterable)
    has_2 = 2 in counts.values()
    has_3 = 3 in counts.values()
    return (has_2, has_3)


def add(x: Tuple, y: Tuple) -> Tuple:
    """
    Example:
    --------
    >>> x = (0,1,2,3)
    >>> y = (3,2,1,0)
    >>> assert list(zip(x,y)) == [(0,3),
                                  (1,2),
                                  (2,1),
                                  (3,0)]
    >>> assert tuple(map(add, zip(x,y))) == (3, 3, 3, 3)
    """
    assert len(x) == len(y)
    reduce_add = partial(reduce, add_)
    return tuple(map(reduce_add, zip(x, y)))


def checksum(iterables: Iterable[Iterable]) -> int:
    has_2_has_3 = reduce(add, map(check, iterables))
    return reduce(mul, has_2_has_3)


def diff(x: Iterable, y: Iterable) -> Iterable:
    """
    Return an Iterable of bools, False when elements of x and y are equal.
    """
    reduce_ne = partial(reduce, ne)
    return map(reduce_ne, zip(x, y))


def subtract(x: Iterable, y: Iterable) -> Iterable:
    return [xi for xi, yi in zip(x, y) if xi == yi]


def correct(iterables: Iterable[Iterable]) -> Optional[Iterable]:
    for x, y in combinations(iterables, 2):
        if sum(diff(x, y)) == 1:
            return subtract(x, y)

    return None


def to_str(x: Iterable[str]) -> str:
    return ''.join(x)


box_ids_1: List[str] = [
    'abcdef',
    'bababc',
    'abbcde',
    'abcccd',
    'aabcdd',
    'abcdee',
    'ababab',
]

box_ids_2: List[str] = [
    'abcde',
    'fghij',
    'klmno',
    'pqrst',
    'fguij',
    'axcye',
    'wvxyz',
]

assert check(box_ids_1[0]) == (0, 0)
assert check(box_ids_1[1]) == (1, 1)
assert check(box_ids_1[2]) == (1, 0)
assert check(box_ids_1[3]) == (0, 1)
assert check(box_ids_1[4]) == (1, 0)
assert check(box_ids_1[5]) == (1, 0)
assert check(box_ids_1[6]) == (0, 1)

assert checksum(box_ids_1) == 12

assert to_str(correct(box_ids_2)) == 'fgij'

inputs = parse_input('data/day_02.txt')
print('First 5 inputs:', inputs[:5])
print('Last 5 inputs:', inputs[-5:])
print('Part 1:', checksum(inputs))
print('Part 2:', to_str(correct(inputs)))
