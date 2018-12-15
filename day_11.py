"""
Notes
-----
Build an array of power levels
Slide a 3x3 window & calculate sum of power levels
"""
import numpy as np
from typing import Tuple


def build_power_levels(serial_no: int) -> np.ndarray:
    n_x = 300
    n_y = 300
    power_levels = np.empty((n_x, n_y), dtype=int)

    for x in range(n_x):
        for y in range(n_y):
            power_levels[x, y] = get_power_level(x + 1, y + 1, serial_no)

    return power_levels


def get_power_level(x: int, y: int, serial_no: int) -> int:
    rack_id = x + 10
    power_level = (rack_id * y + serial_no) * rack_id
    power_level = power_level // 100 % 10 - 5
    return power_level


def get_largest_square(power_levels: np.ndarray,
                       width: int = 3,
                       height: int = 3) -> Tuple[int, int, int]:
    best_x = np.nan
    best_y = np.nan
    best_power_level = -np.inf
    for x in range(0, power_levels.shape[0] - width + 2):
        for y in range(0, power_levels.shape[1] - height + 2):
            square = power_levels[x:(x + width), y:(y + height)]
            power_level = square.sum()
            if power_level > best_power_level:
                best_x = x
                best_y = y
                best_power_level = power_level

    return (best_x + 1, best_y + 1, best_power_level)


def get_largest_total_square(power_levels: np.ndarray):
    best_x = np.nan
    best_y = np.nan
    best_size = np.nan
    best_power_level = -np.inf
    for size in range(100):
        x, y, power_level = get_largest_square(power_levels,
                                               width=size,
                                               height=size)
        if power_level > best_power_level:
            best_x = x
            best_y = y
            best_size = size
            best_power_level = power_level
        elif power_level < 0:
            break

    return (best_x, best_y, best_size, best_power_level)


assert get_power_level(3, 5, 8) == 4
assert get_power_level(122, 79, 57) == -5
assert get_power_level(217, 196, 39) == 0
assert get_power_level(101, 153, 71) == 4

test_power_levels_18 = build_power_levels(18)
assert get_largest_square(test_power_levels_18) == (33, 45, 29)

test_power_levels_42 = build_power_levels(42)
assert get_largest_square(test_power_levels_42) == (21, 61, 30)

assert get_largest_total_square(test_power_levels_18) == (90, 269, 16, 113)
assert get_largest_total_square(test_power_levels_42) == (232, 251, 12, 119)

power_levels = build_power_levels(4455)
print(get_largest_square(power_levels))
print(get_largest_total_square(power_levels))
