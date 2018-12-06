"""
Notes
-----
pos  0123456789012345
poly dabAcCaCBAcCcaDa

pos 1 -> do nothing
pos 2 -> do nothing
pos 3 -> do nothing
pos 4 -> do nothing
pos 5 -> react
new poly input with offset = 4
"""
import string
from collections import Counter
from typing import Optional, Tuple


def react(poly: str, offset: int = 1) -> Tuple[str, Optional[int]]:
    for pos in range(offset, len(poly)):
        prev_unit = poly[pos - 1]
        unit = poly[pos]
        if prev_unit.swapcase() == unit:
            return poly[:(pos - 1)] + poly[(pos + 1):], (pos - 1)
    return poly, None

def fully_react(poly: str) -> str:
    prev_poly = ''
    cur_poly = poly
    offset = 1
    while prev_poly != cur_poly:
        prev_poly = cur_poly
        cur_poly, offset = react(cur_poly, offset)
    return cur_poly

def len_shortest_polymer(poly: str) -> Tuple[str, int]:
    reacted_poly_lengths: Counter = Counter()
    for letter in string.ascii_lowercase:
        removed_poly = poly.replace(letter, '').replace(letter.upper(), '')
        reacted_poly_lengths[letter] = len(fully_react(removed_poly))
    return reacted_poly_lengths.most_common()[-1]


test_polymer = 'dabAcCaCBAcCcaDa'
test_reacted = fully_react(test_polymer)

assert len(test_reacted) == 10
assert len_shortest_polymer(test_polymer) == ('c', 4)


if __name__ == '__main__':
    with open('data/day_05.txt') as file:
        polymer = file.read().strip()

    reacted = fully_react(polymer)
    print(len(reacted))
    print(len_shortest_polymer(polymer))
