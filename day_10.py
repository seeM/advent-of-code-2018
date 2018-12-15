"""
Notes
-----
Not sure how to easily parse characters out of a set of points, so will just
plot the image of the points at each step...

Is that practical?

Points are so far away and move so slowly that this won't work.

Maybe we can narrow down the space, by eg only plotting when there are no
unconnected points (points with no neighbours)
"""

import re
from itertools import count
from typing import List, Tuple

import numpy as np

import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt


POINT_PATTERN = re.compile(r'^'
                           r'position\=\<(\ ?\-?[0-9]+)\, (\ ?\-?[0-9]+)\> '
                           r'velocity\=\<(\ ?\-?[0-9]+)\, (\ ?\-?[0-9]+)\>$')


def parse(lines: List[str]) -> Tuple[np.ndarray, np.ndarray]:
    points: List[Tuple[int, int]] = []
    velocities: List[Tuple[int, int]] = []
    for line in lines:
        match = re.match(POINT_PATTERN, line.strip())
        if match is None:
            raise ValueError('Bad string', line)
        x, y, vx, vy = [int(a) for a in match.groups()]
        points.append((x, y))
        velocities.append((vx, vy))
    return np.array(points), np.array(velocities)


def find_message(points: np.ndarray, velocities: np.ndarray):
    NEIGHBOURS = [(-1, -1), (0, -1), (1, -1),
                  (-1,  0),          (1,  0),
                  (-1,  1), (0,  1), (1,  1)]

    original_points = points

    for step in count():
        points = original_points + step * velocities

        # Maps points to bool, True if the point has neighbour(s)
        has_neighbour = {(p[0], p[1]): False for p in points}

        # Go through all points, if any point has no neighbours, plot
        message = True
        for point in points:
            point = tuple(point)

            if has_neighbour[point]:
                continue

            neighbours = [(n[0] + point[0], n[1] + point[1])
                          for n in NEIGHBOURS]
            for n in neighbours:
                if n in has_neighbour:
                    has_neighbour[n] = True
                    has_neighbour[point] = True

            if not has_neighbour[point]:
                message = False
                break

        if message:
            break

    plot(points).savefig(f'outputs/day_10/{step}')


def plot(points: np.ndarray) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(18, 4))
    ax.plot(points[:, 0], -points[:, 1], '.')
    return fig


with open('data/test_day_10.txt') as f:
    test_points, test_velocities = parse(f.readlines())
    find_message(test_points, test_velocities)


with open('data/day_10.txt') as f:
    points, velocities = parse(f.readlines())
    find_message(points, velocities)


# KZHGRJGZ
# 10932 seconds
